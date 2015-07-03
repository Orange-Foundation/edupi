from django.test import TestCase, Client
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from cntapp.views.views import index
from cntapp.views.custom import sys_info


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
