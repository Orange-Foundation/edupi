import time
from unittest import skip
import json
from datetime import datetime
import shutil
import tempfile
import os
import gzip

from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest

from cntapp.models import Document
from .helpers import PdfDocumentFactory
from cntapp.views.stats import documents_stats, _update_stats, \
    STATS_LOCK_FILE_NAME, StatsLockManager


def current_milliseconds():
    return str(round(time.time() * 1000))


class StatsTest(TestCase):

    def setUp(self):
        self.data = b"""
10.0.0.93 - - [06/Jul/2015:14:29:54 +0000] "GET /media/les_propositions.mp4 HTTP/1.1" 404 198 "http://edupi.fondationorange.org:8021/" "Mozilla/5.0 (Linux; Android 4.4.2; T411 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.111 Safari/537.36"
10.0.0.93 - - [06/Jul/2015:14:29:55 +0000] "GET /media/les_propositions.mp4 HTTP/1.1" 404 198 "http://edupi.fondationorange.org:8021/" "Mozilla/5.0 (Linux; Android 4.4.2; T411 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.111 Safari/537.36"
192.168.1.29 - - [06/Jul/2015:14:30:22 +0000] "GET /media/stats_test.apk HTTP/1.1" 200 524288 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/43.0.2357.81 Chrome/43.0.2357.81 Safari/537.36"
192.168.1.29 - - [06/Jul/2015:14:30:22 +0000] "GET /media/stats_test.apk HTTP/1.1" 200 524288 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/43.0.2357.81 Chrome/43.0.2357.81 Safari/537.36"
192.168.1.29 - - [06/Jul/2015:14:30:23 +0000] "GET /media/stats_test.apk HTTP/1.1" 200 524288 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/43.0.2357.81 Chrome/43.0.2357.81 Safari/537.36"
192.168.1.29 - - [06/Jul/2015:14:30:52 +0000] "GET /media/stats_test.apk HTTP/1.1" 200 524288 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/43.0.2357.81 Chrome/43.0.2357.81 Safari/537.36"
192.168.1.29 - - [06/Jul/2015:14:30:53 +0000] "GET /media/stats_test.apk HTTP/1.1" 200 524288 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/43.0.2357.81 Chrome/43.0.2357.81 Safari/537.36"
192.168.1.29 - - [06/Jul/2015:14:31:01 +0000] "GET /media/stats_test.apk HTTP/1.1" 200 524288 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/43.0.2357.81 Chrome/43.0.2357.81 Safari/537.36"
192.168.1.29 - - [06/Jul/2015:14:31:01 +0000] "GET /media/stats_test.apk HTTP/1.1" 200 524288 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/43.0.2357.81 Chrome/43.0.2357.81 Safari/537.36"
192.168.1.29 - - [06/Jul/2015:14:31:01 +0000] "GET /media/stats_test.apk HTTP/1.1" 200 524288 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/43.0.2357.81 Chrome/43.0.2357.81 Safari/537.36"

192.168.1.29 - - [06/Jul/2015:14:30:56 +0000] "GET /media/puty.apk HTTP/1.1" 404 198 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/43.0.2357.81 Chrome/43.0.2357.81 Safari/537.36"

192.168.1.29 - - [06/Jul/2015:14:31:01 +0000] "GET /media/stats.apk HTTP/1.1" 200 524288 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/43.0.2357.81 Chrome/43.0.2357.81 Safari/537.36"
192.168.1.29 - - [06/Jul/2015:14:31:01 +0000] "GET /media/stats.pdf HTTP/1.1" 200 524288 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/43.0.2357.81 Chrome/43.0.2357.81 Safari/537.36"
192.168.1.29 - - [06/Jul/2015:14:31:01 +0000] "GET /media/stats.pdf HTTP/1.1" 200 524288 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/43.0.2357.81 Chrome/43.0.2357.81 Safari/537.36"
192.168.1.29 - - [06/Jul/2015:14:31:01 +0000] "GET /media/stats.pdf HTTP/1.1" 200 524288 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/43.0.2357.81 Chrome/43.0.2357.81 Safari/537.36"
123123
        """
        self.nginx_log_dir = tempfile.mkdtemp(prefix='edupi_nginx_log_')
        self.doc_1 = PdfDocumentFactory(name='stats_test.apk')
        self.doc_2 = PdfDocumentFactory(name='stats.pdf')
        self.log_files_count = 52

        # prepare one log file, and (self.log_file_count - 1) zipped log files
        log_file = tempfile.mktemp(dir=self.nginx_log_dir,
                                   prefix=settings.NGINX_MEDIA_ACCESS_LOG_PREFIX,
                                   suffix='.log')
        with open(log_file, 'w') as f:
            f.write(self.data.decode())

        for x in range(self.log_files_count - 1):
            zipped_log_file = tempfile.mktemp(dir=self.nginx_log_dir,
                                              prefix=settings.NGINX_MEDIA_ACCESS_LOG_PREFIX,
                                              suffix='.gz')
            with gzip.open(zipped_log_file, 'wb') as zf:
                zf.write(self.data)

    def tearDown(self):
        # must delete the document otherwise there will be unexpected filename for new documents
        self.doc_1.delete()
        self.doc_2.delete()
        shutil.rmtree(self.nginx_log_dir)

    def test_url_resolves_to_stats_json(self):
        found = resolve('/custom/documents_stats/')
        self.assertEqual(found.func, documents_stats)

    def test_update_stats(self):
        log_file = tempfile.mktemp(prefix=settings.NGINX_MEDIA_ACCESS_LOG_PREFIX)
        with open(log_file, mode='w') as f:
            f.write(self.data.decode())

        stats = {}  # shared object
        query_set = Document.objects.all()
        _update_stats(log_file, query_set, stats)

        def check_stats(times):
            self.assertEqual({
                self.doc_1.id: {
                    'name': self.doc_1.name,
                    'file': self.doc_1.file.url,
                    'description': self.doc_1.description,
                    'type': self.doc_1.type,
                    'clicks': 8 * times
                },
                self.doc_2.id: {
                    'name': self.doc_2.name,
                    'file': self.doc_2.file.url,
                    'description': self.doc_2.description,
                    'type': self.doc_2.type,
                    'clicks': 3 * times
                },
            }, stats)

        check_stats(1)

        # calculate twice, the result should accumulate
        _update_stats(log_file, query_set, stats)
        check_stats(2)

        # zip the file, the function can still read it
        zipped_log_file = tempfile.mktemp(prefix=settings.NGINX_MEDIA_ACCESS_LOG_PREFIX, suffix='.gz')
        with gzip.open(zipped_log_file, 'wb') as zf:
            zf.write(self.data)

        # the third update :)
        _update_stats(zipped_log_file, query_set, stats)
        check_stats(3)

        os.remove(log_file)
        os.remove(zipped_log_file)

    def _check_response_content(self, response):
        self.assertEqual(200, response.status_code)
        self.assertEqual({
            str(self.doc_1.id): {"clicks": 8 * self.log_files_count, "name": self.doc_1.name},
            str(self.doc_2.id): {"clicks": 3 * self.log_files_count, "name": self.doc_2.name}
        }, eval(response.content))

    @skip('cannot find a proper way to test multi threading in django')
    def test_start_stats(self):
        if StatsLockManager.is_locked():
            StatsLockManager.unlock()
        now = str(datetime.now())

        self.assertTrue(os.path.exists(self.nginx_log_dir))
        with self.settings(NGINX_LOG_DIR=self.nginx_log_dir):
            response = self.client.get('/custom/stats/start/', data={'stats_date': now})
            self.assertEqual(200, response.status_code)
            self.assertEqual({"status": "started"}, eval(response.content))


class StatsJsonDumpTest(TestCase):

    def adapt_result_to_dict(self, data_list):
        adapted = {}
        for d in data_list:
            adapted[d['id']] = {
                'name': d['name'],
                'description': d['description'],
                'clicks': d['clicks'],
                'type': d['type'],
                'file': d['file']
            }
        return adapted

    def test_get_json_file(self):
        stats = {
            '1': {
                'name': 'test_1',
                'description': '',
                'file': '',
                'type': '',
                'clicks': 8
            },
            '2': {
                'name': 'test_2',
                'description': '',
                'file': '',
                'type': '',
                'clicks': 3
            },
        }
        now = current_milliseconds()
        filename = now + '.json'
        stats_file_path = os.path.join(settings.STATS_DIR, filename)
        with open(stats_file_path, 'w') as f:
            f.write(json.dumps(stats))

        response = self.client.get('/custom/documents_stats/', data={'stats_date': now})
        self.assertEqual(200, response.status_code)

        self.assertEqual(stats, self.adapt_result_to_dict(eval(response.content)))
        os.remove(stats_file_path)


class RunStatsTest(TestCase):

    def test_scenario(self):
        now = current_milliseconds()
        json_file_path = os.path.join(settings.STATS_DIR, now + '.json')
        self.assertFalse(os.path.exists(json_file_path))

        resp_0 = self.client.get('/custom/stats/status/', data={'stats_date': now})
        self.assertEqual({'status': 'idle'}, eval(resp_0.content))

        # no log file
        nginx_log_dir = tempfile.mkdtemp(prefix='edupi_nginx_log_')

        # start running
        with self.settings(NGINX_LOG_DIR=nginx_log_dir):
            response = self.client.get('/custom/stats/start/', data={'stats_date': now})

        self.assertEqual(200, response.status_code)
        self.assertEqual({'status': 'started'}, eval(response.content))

        # FIXME: not sure if this will run before starting the thread at each time.
        # resp_1 = self.client.get('/custom/stats/status/', data={'stats_date': now})
        # self.assertEqual({'status': 'running'}, eval(resp_1.content))

        time.sleep(0.5)  # wait for a moment

        # check if it's finished
        resp_2 = self.client.get('/custom/stats/status/', data={'stats_date': now})
        self.assertEqual({'status': 'finished'}, eval(resp_2.content))

        # check if the json file is created
        self.assertTrue(os.path.exists(json_file_path))

        # get json response
        json_stats_resp = self.client.get('/custom/documents_stats/', data={'stats_date': now})
        self.assertEqual(200, json_stats_resp.status_code)
        self.assertEqual([], eval(json_stats_resp.content))


class StatsStatusTest(TestCase):

    def test_running(self):
        # ATTENTION:
        # Reload stats module run the test with a separated settings.STATS_DIR.
        # this is because stats.StatsLockManager was imported in apps.py once,
        # which is taken place before runner.py
        import importlib
        from cntapp.views import stats
        importlib.reload(stats)

        lock_file = os.path.join(settings.STATS_DIR, STATS_LOCK_FILE_NAME)
        if not os.path.exists(lock_file):
            open(lock_file, 'a').close()

        now = current_milliseconds()
        response = self.client.get('/custom/stats/status/', data={'stats_date': now})
        self.assertEqual(200, response.status_code)
        self.assertEqual({'status': 'running'}, eval(response.content))
        os.remove(lock_file)

    def test_finished(self):
        lock_file = os.path.join(settings.STATS_DIR, STATS_LOCK_FILE_NAME)
        if os.path.exists(lock_file):
            os.remove(lock_file)
        now = datetime.now().time()
        os.system('touch %s' % (os.path.join(settings.STATS_DIR, str(now) + '.json')))
        response = self.client.get('/custom/stats/status/', data={'stats_date': now})
        self.assertEqual(200, response.status_code)
        self.assertEqual({'status': 'finished'}, eval(response.content))

    def test_idle(self):
        lock_file = os.path.join(settings.STATS_DIR, STATS_LOCK_FILE_NAME)
        if os.path.exists(lock_file):
            os.remove(lock_file)
        now = datetime.now().time()
        response = self.client.get('/custom/stats/status/', data={'stats_date': now})
        self.assertEqual(200, response.status_code)
        self.assertEqual({'status': 'idle'}, eval(response.content))


class StatsLockManagerTest(TestCase):

    def test_lock_unlock(self):
        from cntapp.views.stats import logger
        if StatsLockManager.is_locked():
            StatsLockManager.unlock()
        self.assertFalse(StatsLockManager.is_locked())

        StatsLockManager.lock()
        self.assertTrue(StatsLockManager.is_locked())

        with self.assertLogs(logger=logger, level='ERROR') as m:
            StatsLockManager.lock()
            self.assertTrue(StatsLockManager.is_locked())
            self.assertIn('.running.lock" already exists!', m.output[0])

        StatsLockManager.unlock()
        self.assertFalse(StatsLockManager.is_locked())

        with self.assertLogs(logger=logger, level='ERROR') as m:
            StatsLockManager.unlock()
            self.assertFalse(StatsLockManager.is_locked())
            self.assertIn('.running.lock" not found!', m.output[0])


class StatsFilesTest(TestCase):

    def test_list_and_delete_stats(self):
        stats_date = current_milliseconds()
        filename = stats_date + '.json'
        test_file_path = os.path.join(settings.STATS_DIR, filename)
        open(test_file_path, 'a').close()

        resp = self.client.get('/custom/stats/')
        self.assertIn(filename, eval(resp.content))

        resp2 = self.client.delete('/custom/stats/', data={'stats_date': stats_date})
        self.assertEqual(204, resp2.status_code)

        resp3 = self.client.get('/custom/stats/')
        self.assertNotIn(filename, eval(resp3.content))

    def test_stats_regex(self):
        from cntapp.views.stats import STATS_REGEX
        s = """192.168.1.29 - - [06/Jul/2015:14:30:22 +0000] "GET /media/stats_test.apk HTTP/1.1" 200 524288 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/43.0.2357.81 Chrome/43.0.2357.81 Safari/537.36"
        """
        self.assertIsNotNone(STATS_REGEX.match(s))

        s = """192.168.1.29 - - [06/Jul/2015:14:30:22 +0000] "GET /media/thumbnail/stats_test.apk HTTP/1.1" 200 524288 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/43.0.2357.81 Chrome/43.0.2357.81 Safari/537.36"
        """
        self.assertIsNone(STATS_REGEX.match(s))
