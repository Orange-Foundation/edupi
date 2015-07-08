import shutil
import tempfile
import os
import gzip

from django.conf import settings
from django.test import TestCase, Client
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from cntapp.models import Document
from .helpers import PdfDocumentFactory
from cntapp.views.views import index
from cntapp.views.custom import sys_info, documents_stats, _update_stats


class IndexPageTest(TestCase):

    def test_root_url_resolves_to_index_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, index)

    def test_index_page_returns_correct_html(self):
        request = HttpRequest()
        response = index(request)
        # assure it works in mobile device
        self.assertIn('<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">',
                      response.content.decode())
        self.assertEqual(response.content.decode(), render_to_string('cntapp/index.html'))


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
        self.nginx_dir = tempfile.mkdtemp(prefix='edupi_nginx_log_')
        # self.media_root = tempfile.mkdtemp(prefix='edupi_media_root_')
        self.doc_1 = PdfDocumentFactory(name='stats_test.apk')
        self.doc_2 = PdfDocumentFactory(name='stats.pdf')
        self.log_files_count = 52

        # prepare one log file, and (self.log_file_count - 1) zipped log files
        log_file = tempfile.mktemp(dir=self.nginx_dir, prefix=settings.NGINX_MEDIA_ACCESS_LOG_PREFIX, suffix='.log')
        with open(log_file, 'w') as f:
            f.write(self.data.decode())

        for x in range(self.log_files_count - 1):
            zipped_log_file = tempfile.mktemp(dir=self.nginx_dir, prefix=settings.NGINX_MEDIA_ACCESS_LOG_PREFIX, suffix='.gz')
            with gzip.open(zipped_log_file, 'wb') as zf:
                zf.write(self.data)

    def tearDown(self):
        # must delete the document otherwise there will be unexpected filename for new documents
        self.doc_1.delete()
        self.doc_2.delete()
        shutil.rmtree(self.nginx_dir)

    def test_url_resolves_to_stats_json(self):
        found = resolve('/custom/documents_stats/')
        self.assertEqual(found.func, documents_stats)

    def test_update_stats(self):
        log_file = tempfile.mktemp(prefix=settings.NGINX_MEDIA_ACCESS_LOG_PREFIX)
        with open(log_file, mode='w') as f:
            f.write(self.data.decode())

        docs = Document.objects.all()
        stats = {}  # shared object
        _update_stats(log_file, stats)
        self.assertEqual({
            self.doc_1.id: {
                'name': self.doc_1.name,
                'clicks': 8
            },
            self.doc_2.id: {
                'name': self.doc_2.name,
                'clicks': 3
            },
        }, stats)

        # calculate twice, the result should accumulate
        _update_stats(log_file, stats)
        self.assertEqual({
            self.doc_1.id: {
                'name': self.doc_1.name,
                'clicks': 8 * 2
            },
            self.doc_2.id: {
                'name': self.doc_2.name,
                'clicks': 3 * 2
            },
        }, stats)

        # zip the file, the function can still read it
        zipped_log_file = tempfile.mktemp(prefix=settings.NGINX_MEDIA_ACCESS_LOG_PREFIX, suffix='.gz')
        with gzip.open(zipped_log_file, 'wb') as zf:
            zf.write(self.data)

        # the third update :)
        _update_stats(zipped_log_file, stats)
        self.assertEqual({
            self.doc_1.id: {
                'name': self.doc_1.name,
                'clicks': 8 * 3
            },
            self.doc_2.id: {
                'name': self.doc_2.name,
                'clicks': 3 * 3
            },
        }, stats)
        os.remove(log_file)
        os.remove(zipped_log_file)

    def _check_response_content(self, response):
        self.assertEqual(200, response.status_code)
        self.assertEqual({
            str(self.doc_1.id): {"clicks": 8 * self.log_files_count, "name": self.doc_1.name},
            str(self.doc_2.id): {"clicks": 3 * self.log_files_count, "name": self.doc_2.name}
        }, eval(response.content))

    def test_document_stats_view(self):
        with self.settings(NGINX_LOG_DIR=self.nginx_dir):
            response = documents_stats(HttpRequest())
            self._check_response_content(response)

    def test_documents_stats_ajax(self):
        with self.settings(NGINX_LOG_DIR=self.nginx_dir):
            response = self.client.get('/custom/documents_stats/')
            self._check_response_content(response)


class SysInfoTest(TestCase):

    def checkSysInfoContent(self, content):
        self.assertIn('cntapp', content)
        self.assertIn('fileSystem', content)
        self.assertIn('CurrentVersion', content)

        cntapp_info = content['cntapp']
        self.assertIn('Used', cntapp_info)
        self.assertIn('TotalDocumentsReferences', cntapp_info)
        self.assertIn('TotalDocuments', cntapp_info)

        file_sys_info = content['fileSystem']
        self.assertIn('Used', file_sys_info)
        self.assertIn('TotalSize', file_sys_info)
        self.assertIn('Available', file_sys_info)
        self.assertIn('UsedPercentage', file_sys_info)

    def test_sys_info(self):
        request = HttpRequest()
        res = sys_info(request)
        self.checkSysInfoContent(eval(res.content))

    def test_sys_info_ajax(self):
        client = Client()
        res = client.get('/custom/sys_info/')
        self.checkSysInfoContent(eval(res.content))
