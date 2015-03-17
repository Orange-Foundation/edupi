from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver


class FunctionalTest(StaticLiveServerTestCase):

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
