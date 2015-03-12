from selenium import webdriver
import unittest


class IndexPageTest(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()
        super().tearDown()

    def test_visit_home_page(self):
        self.browser.get('http://127.0.0.1:8000')
        self.assertIn('Edupi', self.browser.title)
