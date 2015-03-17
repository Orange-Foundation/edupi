import sys

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver


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
    def tearDown(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        super().setUp()
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()
        super().tearDown()

    def assertInBody(self, text):
        self.assertIn(text, self.browser.find_element_by_tag_name('body').text)

    def assertNotInBody(self, text):
        self.assertNotIn(text, self.browser.find_element_by_tag_name('body').text)
