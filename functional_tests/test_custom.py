from cntapp.models import Directory
from selenium import webdriver
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from .base import FunctionalTest


class CustomSiteTestCase(FunctionalTest):

    def setUp(self):
        super().setUp()
        self.custom_page_url = self.server_url + '/custom/'

    def create_dir(self, dir_name):
        self.assertNotInBody(dir_name)
        base_url = self.browser.current_url

        # entered into a create page
        self.browser.find_element_by_id("create-directory").click()

        if base_url == self.custom_page_url:
            self.assertEqual(base_url + "#create", self.browser.current_url)
        else:
            self.assertEqual(base_url + "/create", self.browser.current_url)

        self.assertInBody("Create directory")

        # create directory
        self.browser.find_element_by_id('directory-name').send_keys(dir_name)
        self.browser.find_element_by_id('btn-create').send_keys(Keys.ENTER)

        # automatically go back to previous page
        self.assertEqual(base_url, self.browser.current_url)
        self.assertInBody(dir_name)

    def test_create_directories(self):
        # Alice wants to customize the web site, she enters into the custom home page
        self.browser.get(self.custom_page_url)
        self.assertInBody("Content Manager")

        # she is currently in the root dir, it's empty, she has to create a dir here
        # she clicks "Create Directory" to enter the create page,
        # she types a dir name in the input field and hit "ENTER",
        # then create form disappeared, and the name appears
        self.create_dir("primary")
        self.create_dir("secondary")

        # click the primary to go into this folder
        self.browser.find_element_by_link_text('primary').click()

        self.assertNotInBody("primary")
        self.assertNotInBody("secondary")

        self.create_dir("CP")
        self.create_dir("CE1")

        # enter in the next level
        self.browser.find_element_by_link_text('CP').click()
        self.assertNotInBody("CP")

        self.create_dir("Math")
        self.create_dir("English")
        self.create_dir("French")

        self.browser.get(self.custom_page_url)
        self.assertInBody("primary")
        self.assertNotInBody("Math")

    def test_edit_directory(self):
        from cntapp.tests.helpers import init_test_dirs
        init_test_dirs()
        ## Let's get edit dir "a", and change it's name to primary

        # go into the root dirs page
        self.browser.get(self.custom_page_url)
        self.assertNotInBody("primary")

        edit_elements = self.browser.find_elements_by_name("edit")
        self.assertEqual(3, len(edit_elements))

        edit_dir_a = edit_elements[0]
        href = edit_dir_a.get_attribute("href")

        # go into directory's edit page
        edit_dir_a.click()
        self.assertEqual(href, self.browser.current_url)
        self.assertInBody("Edit directory")

        # verify that the name is pre-filled
        name_input = self.browser.find_element_by_name("name")
        self.assertEqual("a", name_input.get_attribute("value"))

        # change the name
        name_input.clear()
        name_input.send_keys("primary")
        self.browser.find_element_by_id("submit").click()

        self.assertEqual(self.custom_page_url, self.browser.current_url)
        self.assertInBody("primary")

