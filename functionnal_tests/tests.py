from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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
        h1_tags = self.browser.find_elements_by_tag_name('h1')
        self.assertEqual(len(h1_tags), 1)
        self.assertEqual(h1_tags[0].text, 'Edupi\nWe all need to learn')
        btn_start = self.browser.find_element_by_tag_name('a')
        self.assertEqual(btn_start.text, 'Get started')
