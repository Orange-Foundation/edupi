from selenium import webdriver
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from .base import FunctionalTest


class CustomSiteTestCase(FunctionalTest):

    def check_create_dir(self, dir_name):
        self.assertNotInBody(dir_name)
        self.browser.find_element_by_id('id_name').send_keys(dir_name)
        self.browser.find_element_by_id('id_name').send_keys(Keys.ENTER)
        self.assertInBody(dir_name)

    def test_create_directories(self):
        # Alice wants to customize the web site, she enters into the custom home page
        custom_page_url = self.live_server_url + '/custom/'
        self.browser.get(custom_page_url)

        # she is currently in the root dir, it's empty, she has to create a dir here
        # she types a dir name in the input field and hit "ENTER", then the name appears
        self.check_create_dir('primary')

        # click the primary to go into this folder
        self.browser.find_element_by_link_text('primary').click()
        self.assertEqual(custom_page_url + 'primary/', self.browser.current_url)

        # create two folders in 'primary'
        self.check_create_dir('CP')
        self.check_create_dir('CE1')

        # click 'CP' and create another folder inside
        self.check_create_dir('MATH')
