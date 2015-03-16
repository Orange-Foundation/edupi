from django.test import TestCase
from django.core.urlresolvers import resolve

from cntapp.views.custom import index, resolve_dirs_structure
from cntapp.tests.helpers import init_test_dirs


class CustomUrlsResolveTestCase(TestCase):

    def test_index(self):
        found = resolve('/custom/')
        self.assertEqual(found.func, index)

    def test_levels(self):
        init_test_dirs()
        urls = ['/custom/a/', '/custom/a_a/', '/custom/a/a_a_a/']
        map(self.assertEqual, zip([resolve(u).func for u in urls], [resolve_dirs_structure] * len(urls)))
