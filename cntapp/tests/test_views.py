from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from cntapp.views.views import index


class IndexPageTestCase(TestCase):

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