from selenium import webdriver
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from .base import FunctionalTest


class CustomSiteTestCase(FunctionalTest):

    def test_create_directories(self):
        # Alice wants to customize the web site, she enters into the custom home page
        custom_page_url = self.live_server_url + '/custom/'
        self.browser.get(custom_page_url)

        # she is currently in the root dir, it's empty, she has to create a dir here
        self.assertNotInBody('primary')

        # She types a dir name in the input field
        # then she clicks the button "create folder"
        self.browser.find_element_by_id('id_input_new_dir').send_keys('primary')
        self.browser.find_element_by_id('id_create_dir').click()

        # she sees the name appears
        self.assertInBody('primary')

        # click the primary to go into this folder
        primary_link = self.browser.find_element_by_link_text('primary')
        primary_link.click()

        self.assertEqual(custom_page_url + 'primary/', self.browser.current_url)

        # type name in input box and click the button to create a folder inside primary
        self.assertNotInBody('CP')
        self.browser.find_element_by_id('id_input_new_dir').send_keys('CP')
        self.browser.find_element_by_id('id_create_dir').click()
        self.assertInBody('CP')

        # she also create a folder by hitting ENTER directly
        self.assertNotIn('CE1', self.browser.find_element_by_id('id_dirs').text)
        input_box = self.browser.find_element_by_id('id_input_new_dir')
        input_box.send_keys('CE1')
        input_box.send_keys(Keys.ENTER)
        self.assertIn('CP', self.browser.find_element_by_id('id_dirs').text)

        self.fail("Finish the test!")
