from django.test import TestCase
from django.core.urlresolvers import resolve

from cntapp.views.custom import index


class CustomUrlsResolveTest(TestCase):

    def test_index(self):
        found = resolve('/custom/')
        self.assertEqual(found.func, index)
