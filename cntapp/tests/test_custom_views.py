from django.contrib.auth import get_user_model
from django.test import TestCase

from .helpers import init_test_dirs

User = get_user_model()


class DirsCustomTest(TestCase):

    def setUp(self):
        self.username = 'yuancheng'
        self.password = 'secret'
        self.user = User.objects.create_superuser(username=self.username, email='', password=self.password)

    def login(self):
        if not self.client.login(username=self.username, password=self.password):
            self.fail('Admin is not login')

    def test_uses_index_template(self):
        init_test_dirs()
        self.login()
        response = self.client.get('/custom/')
        self.assertTemplateUsed(response, 'cntapp/custom/index.html')

    def test_redirect_to_login(self):
        response = self.client.get('/custom/')
        self.assertRedirects(response, '/custom/login/')

    def test_logout_redirect(self):
        self.login()
        response = self.client.get('/custom/logout/')
        self.assertRedirects(response, '/custom/login/')
