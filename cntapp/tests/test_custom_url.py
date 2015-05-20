from django.test import TestCase
from django.core.urlresolvers import resolve

from cntapp.views.custom import index, login_page, logout_admin


class CustomUrlsResolveTest(TestCase):

    def test_index(self):
        found = resolve('/custom/')
        self.assertEqual(found.func, index)

    def test_login(self):
        found = resolve('/custom/login/')
        self.assertEqual(found.func, login_page)

    def test_logout(self):
        found = resolve('/custom/logout/')
        self.assertEqual(found.func, logout_admin)
