from selenium import webdriver
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys


class IndexPageTest(LiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()
        super().tearDown()

    def test_visit_index_page(self):
        # enter into index page
        self.browser.get(self.live_server_url)

        # checkout the 'get started' link
        link = self.browser.find_element_by_id('id_get_started')
        self.assertEqual(link.get_attribute(name='href'), self.live_server_url + '/dirs/')

        link.click()

        # go to browse the directories
        self.assertEqual(self.browser.current_url, self.live_server_url + '/dirs/')


class CustomSiteTestCase(LiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()
        super().tearDown()

    def test_create_directories(self):
        # Alice wants to customize the web site, she enters into the custom home page
        custom_page_url = self.live_server_url + '/custom/'
        self.browser.get(custom_page_url)

        # she is currently in the root dir, it's empty, she has to create a dir here
        # She types a dir name in the input field

        self.assertIsNotNone(self.browser.find_element_by_id('id_empty'))
        input_box = self.browser.find_element_by_id('id_input_new_dir')
        input_box.send_keys('primary')

        # then she clicks the button "create folder"
        btn_create = self.browser.find_element_by_id('id_create_dir')
        btn_create.click()

        # she sees the name appears
        dirs = self.browser.find_element_by_id('id_dirs')
        self.assertIn('primary', dirs)

        self.fail("Finish the test!")
