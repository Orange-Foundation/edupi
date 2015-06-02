import sys

from django.contrib.auth import get_user_model
from selenium.common.exceptions import NoSuchElementException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from django.core.cache import cache


User = get_user_model()

class FunctionalTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        super().setUp()
        self.username = 'yuancheng'
        self.password = 'secret'
        self.user = User.objects.create_superuser(username=self.username, email='', password=self.password)
        self.browser = webdriver.Firefox()
        cache.clear()

    def tearDown(self):
        self.browser.quit()
        super().tearDown()

    def assertInBody(self, text):
        self.assertIn(text, self.browser.find_element_by_tag_name('body').text)

    def assertNotInBody(self, text):
        self.assertNotIn(text, self.browser.find_element_by_tag_name('body').text)

    def assertElementNotInDOM(self, css_selector):
        try:
            self.browser.find_element_by_css_selector(css_selector)
            self.fail()
        except NoSuchElementException:
            pass
