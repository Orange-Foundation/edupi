import glob
from enum import Enum  # python 3.4
import json
import threading
import gzip
import os
import re
import logging

from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.conf import settings

from cntapp.models import Document


logger = logging.getLogger(__name__)

STATS_LOCK_FILE_NAME = '.running.lock'
STATS_REGEX = re.compile('.*\"GET (/media/([^/]*)) HTTP/1.1\" 200 .*')
STATS_FILE_PATTERN = re.compile('[0-9]{13}\.json')  # milliseconds.json


class StatsLockManager(object):

    lock_path = os.path.join(settings.STATS_DIR, STATS_LOCK_FILE_NAME)

    @classmethod
    def is_locked(cls):
        return os.path.exists(cls.lock_path)

    @classmethod
    def lock(cls):
        if os.path.exists(cls.lock_path):
            logger.error('"%s" already exists!' % cls.lock_path)
        open(cls.lock_path, 'a').close()

    @classmethod
    def unlock(cls):
        if os.path.exists(cls.lock_path):
            os.remove(cls.lock_path)
        else:
            logger.error('lock file "%s" not found!' % cls.lock_path)


class Status(Enum):
    idle = 1
    running = 2
    finished = 3


class StatsWorker(threading.Thread):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        if 'json_file_name' not in kwargs.keys():
            raise Exception('"json_file_name" is not given when initiate')

        self.json_file_name = kwargs['json_file_name']
        self.nginx_log_dir = settings.NGINX_LOG_DIR
        self.nginx_media_access_log_prefix = settings.NGINX_MEDIA_ACCESS_LOG_PREFIX
        # self.query_set = Document.objects.all()
        # catch a snapshot of the database
        self.query_set = Document.objects.get_queryset()

    def run(self):
        # LOCK the process
        if StatsLockManager.is_locked():
            msg = 'Starting a stats worker while there already one running!'
            logger.critical(msg)
            raise Exception(msg)

        StatsLockManager.lock()
        try:
            log_files = [os.path.join(self.nginx_log_dir, filename)
                         for filename in os.listdir(self.nginx_log_dir)
                         if filename.startswith(self.nginx_media_access_log_prefix)]

            stats = {}
            logger.info('log files path:' + str(self.nginx_log_dir))
            logger.info('log files:' + str(log_files))
            for file in log_files:
                _update_stats(file, self.query_set, stats)

            json_file_path = os.path.join(settings.STATS_DIR, self.json_file_name)
            with open(json_file_path, 'w') as f:
                f.write(json.dumps(stats))
        finally:
            # RELEASE the lock
            StatsLockManager.unlock()


@csrf_exempt
def start_stats(request):
    if 'stats_date' not in request.GET.keys():
        return HttpResponseBadRequest('"stats_date" is not provided.')

    json_file_name = request.GET['stats_date'] + '.json'

    # check if there is a worker running, lock
    status = _get_stats_process_status(json_file_name)
    if status == Status.running:
        return HttpResponseBadRequest('a stats worker running.')

    elif status == Status.finished:
        return JsonResponse({'status': 'finished'})

    elif status == Status.idle:
        StatsWorker(kwargs={
            'json_file_name': json_file_name
        }).start()
        return JsonResponse({'status': 'started'})
    else:
        return HttpResponse(status=500)  # internal error


def get_stats_status(request):
    if 'stats_date' in request.GET.keys():
        json_file_name = request.GET['stats_date'] + '.json'
        st = _get_stats_process_status(json_file_name)
        if st == Status.running:
            return JsonResponse({'status': 'running'})
        elif st == Status.finished:
            return JsonResponse({'status': 'finished'})
        elif st == Status.idle:
            return JsonResponse({'status': 'idle'})
    else:
        if StatsLockManager.is_locked():
            return JsonResponse({'status': 'running'})
        else:
            return JsonResponse({'status': 'idle'})


def documents_stats(request):
    if 'stats_date' not in request.GET.keys():
        return HttpResponseBadRequest('"stats_date" is not provided.')

    json_filename = request.GET['stats_date'] + '.json'
    json_file_path = os.path.join(settings.STATS_DIR, json_filename)

    if not os.path.exists(json_file_path):
        return HttpResponseBadRequest('stats file not exist!')

    def adapt_json_to_list(data):
        ret = []
        for k, v in data.items():
            ret.append({
                'id': k,
                'name': v['name'],
                'clicks': v['clicks'],
                'description': v['description'],
                'file': v['file'],
                'type': v['type']
            })
        return ret

    return JsonResponse(adapt_json_to_list(_get_stats(json_file_path)), safe=False)


def stats(request):
    if request.method == 'GET':
        return _list_stats(request)
    elif request.method == 'DELETE':
        return _delete_stats(request)
    else:
        return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)


def _list_stats(request):
    # get all json stats file
    # file are named as MILLISECONDS.json
    files = [
        os.path.split(f)[1]
        for f in glob.glob(os.path.join(settings.STATS_DIR, '*.json'))
    ]

    files = [f for f in files if STATS_FILE_PATTERN.match(f) is not None]
    return JsonResponse(files, safe=False)


def _delete_stats(request):
    body = eval(request.body)
    if 'stats_date' not in body.keys():
        return HttpResponseBadRequest('no stats_date provided')

    json_file = body['stats_date'] + '.json'
    json_file_path = os.path.join(settings.STATS_DIR, json_file)
    if not os.path.exists(json_file_path):
        return HttpResponseBadRequest('"%s" does not exist!')

    try:
        os.remove(json_file_path)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        logger.critical(e)
        return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def _get_stats_process_status(json_file_name):
    stats_dir = settings.STATS_DIR
    if StatsLockManager.is_locked():
        return Status.running
    else:
        if os.path.exists(os.path.join(stats_dir, json_file_name)):
            return Status.finished
        else:
            return Status.idle  # no process is running, the demanded stats is not generated


def _get_stats(json_file_path):
    with open(json_file_path) as f:
        return eval(f.read())


def _update_stats(log_file_path, query_set, stats):
    if not isinstance(stats, dict):
        raise TypeError()

    logger.info('update stats with:"%s"' % log_file_path)

    def _record_stat(match):
        if match is None:
            return

        media_file = './' + match.group(2)
        try:
            d = query_set.get(file=media_file)
            if d.id not in stats.keys():
                stats[d.id] = {
                    'name': d.name,
                    'description': d.description,
                    'type': d.type,
                    'file': d.file.url,
                    'clicks': 1,
                }
            else:
                stats[d.id]['clicks'] += 1
        except Document.DoesNotExist as e:
            logger.warn('no document found for file "%s"' % media_file)

    if log_file_path.endswith('.gz'):
        with gzip.open(log_file_path) as log_file:
            for line in log_file:
                _record_stat(STATS_REGEX.match(line.decode()))
    else:
        with open(log_file_path) as log_file:
            for line in log_file:
                _record_stat(STATS_REGEX.match(line))
    return stats
