import logging
import gzip
import os
import subprocess
import re

from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.conf import settings

from edupi import VERSION
from cntapp.models import Document, Directory


logger = logging.getLogger(__name__)

STATS_REGEX = re.compile(".*\"GET (/media/([^ ]*)) HTTP/1.1\" 200 .*")


def index(request):
    user = request.user
    if user is not None and user.is_superuser and user.is_authenticated():
        return render(request, 'cntapp/custom/index.html')
    else:
        return HttpResponseRedirect(reverse('cntapp:login'))


def login_page(request):
    if request.method != 'POST':
        return render(request, 'cntapp/custom/login.html')

    try:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('cntapp:index'))
        else:
            # the user is not authenticated with the given username and password
            return HttpResponseRedirect(reverse('cntapp:login'))

    except Exception as e:
        return HttpResponseRedirect(reverse('cntapp:login'))


def logout_admin(request):
    logout(request)
    return HttpResponseRedirect(reverse('cntapp:login'))


def sys_info(request):
    """
    Return system information in JSON
    """
    info = {}
    cntapp_info = {}
    system_info = {}

    df_index = {
        "size": 0,
        "used": 1,
        "available": 2,
        "used_percentage": 3,
    }

    # result in k-bytes
    df_res = subprocess.check_output(['df', '/home/']).decode().split()[8:-1]
    system_info["TotalSize"] = df_res[df_index['size']]
    system_info["Used"] = df_res[df_index['used']]
    system_info["Available"] = df_res[df_index['available']]
    system_info["UsedPercentage"] = df_res[df_index['used_percentage']]

    cntapp_info["Used"] = subprocess.check_output(['du', '-s', settings.MEDIA_ROOT]).decode().split()[0]
    cntapp_info['TotalDocuments'] = Document.objects.all().count()
    cntapp_info['TotalDocumentsReferences'] = Directory.documents.through.objects.count()
    cntapp_info['TotalDirectories'] = Directory.objects.all().count()

    info['CurrentVersion'] = VERSION
    info['cntapp'] = cntapp_info
    info['fileSystem'] = system_info
    return JsonResponse(info)


def _update_stats(log_file_path, stats):
    if not isinstance(stats, dict):
        raise TypeError()

    logger.debug('update stats with:"%s"' % log_file_path)

    def _record_stat(match):
        if match is None:
            return

        media_file = './' + match.group(2)
        try:
            d = Document.objects.get(file=media_file)
            if d.id not in stats.keys():
                stats[d.id] = {
                    'name': d.name,
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


def documents_stats(request):
    log_files = [os.path.join(settings.NGINX_LOG_DIR, filename)
                 for filename in os.listdir(settings.NGINX_LOG_DIR)
                 if filename.startswith(settings.NGINX_MEDIA_ACCESS_LOG_PREFIX)]
    stats = {}
    for file in log_files:
        _update_stats(file, stats)

    return JsonResponse(stats)
