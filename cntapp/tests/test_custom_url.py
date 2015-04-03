from django.test import TestCase
from django.core.urlresolvers import resolve

from cntapp.views.custom import index, resolve_dirs_structure
from cntapp.tests.helpers import init_test_dirs


class CustomUrlsResolveTest(TestCase):

    def test_index(self):
        found = resolve('/custom/')
        self.assertEqual(found.func, index)
