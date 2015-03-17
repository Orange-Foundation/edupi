from django.test import TestCase

from cntapp.tests.helpers import init_test_dirs
from cntapp.helpers import get_dir_by_path


class ModelsHelpersTest(TestCase):

    def test_get_url_by_path(self):
        init_test_dirs()
        d = get_dir_by_path('a/ab_a/ab_a_a')
        self.assertEqual('ab_a_a', d.name)
