from django.test import TestCase

from .helpers import init_test_dirs


class DirsCustomTest(TestCase):

    def test_uses_index_template(self):
        init_test_dirs()
        response = self.client.get('/custom/')
        self.assertTemplateUsed(response, 'cntapp/custom/index.html')
