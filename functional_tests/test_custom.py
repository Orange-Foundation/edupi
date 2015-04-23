import os

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from cntapp.models import Directory, Document
from .base import FunctionalTest
from cntapp.tests.helpers import DocumentFactory, init_test_dirs, PdfDocumentFactory


class CustomSiteTestCase(FunctionalTest):

    def setUp(self):
        super().setUp()
        self.custom_page_url = self.server_url + '/custom/'
        self.directories_root_url = self.custom_page_url + '#directories'

    def create_dir(self, dir_name):
        self.assertNotInBody(dir_name)
        base_url = self.browser.current_url

        # entered into a create page
        self.browser.find_element_by_id("create-directory").click()

        self.assertEqual(base_url + "/create", self.browser.current_url)

        self.assertInBody("Create directory")

        # create directory
        self.browser.find_element_by_id('directory-name').send_keys(dir_name)
        self.browser.find_element_by_id('btn-create').send_keys(Keys.ENTER)

        # automatically go back to previous page
        self.assertEqual(base_url, self.browser.current_url)
        self.assertInBody(dir_name)

    def assertNotInDirectoryTable(self, text):
        self.assertNotIn(text, self.browser.find_element_by_css_selector('.table tbody').text)

    def assertInDirectoryTable(self, text):
        self.assertIn(text, self.browser.find_element_by_css_selector('.table tbody').text)

    def go_to_directories(self):
        self.browser.get(self.custom_page_url + "#directories")
        # need some time to load the page
        WebDriverWait(self.browser, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME, "table"))
        )

    def test_create_directories(self):
        # Alice wants to customize the web site, she enters into the custom home page
        self.go_to_directories()

        # she is currently in the root dir, it's empty, she has to create a dir here
        # she clicks "Create Directory" to enter the create page,
        # she types a dir name in the input field and hit "ENTER",
        # then create form disappeared, and the name appears
        self.create_dir("primary")
        self.create_dir("secondary")

        # click the primary to go into this folder
        self.browser.find_element_by_link_text('primary').click()

        self.assertNotInDirectoryTable("primary")
        self.assertNotInDirectoryTable("secondary")

        self.create_dir("CP")
        self.create_dir("CE1")

        # enter in the next level
        self.browser.find_element_by_link_text('CP').click()
        self.assertNotInDirectoryTable("CP")

        self.create_dir("Math")
        self.create_dir("English")
        self.create_dir("French")

        self.go_to_directories()
        self.assertInDirectoryTable("primary")
        self.assertNotInDirectoryTable("Math")

    def enter_into_dir(self, dir_name):
        table = self.browser.find_element_by_id("directories-table")
        table.find_element_by_link_text(dir_name).click()

    def test_navigate_directory_path(self):
        init_test_dirs()
        self.assertEqual(6, Directory.objects.count())
        # check_path = lambda path: self.assertEqual(path, self.browser.find_element_by_id("path").text)

        def check_path(path_list):
            pe = self.browser.find_element_by_css_selector("div#path ol")
            links_text = pe.find_elements_by_css_selector('li')
            for i in range(len(path_list)):
                self.assertEqual(path_list[i], links_text[i].text)

        def back_to_dir(dir_name):
            path = self.browser.find_element_by_id("path")
            path.find_element_by_link_text(dir_name).click()

        self.go_to_directories()

        self.enter_into_dir("a")
        check_path(['home', 'a'])
        self.enter_into_dir("ab_a")
        check_path(['home', 'a', 'ab_a'])
        self.enter_into_dir("ab_a_a")
        check_path(['home', 'a', 'ab_a', 'ab_a_a'])

        self.browser.refresh()
        WebDriverWait(self.browser, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME, "table"))
        )

        check_path(['home', 'a', 'ab_a', 'ab_a_a'])

        back_to_dir("ab_a")
        check_path(['home', 'a', 'ab_a'])
        back_to_dir("a")
        check_path(['home', 'a'])
        back_to_dir("home")
        self.enter_into_dir("a")
        check_path(['home', 'a'])
        self.assertEqual(6, Directory.objects.count())

    def test_edit_directory(self):
        init_test_dirs()
        ## Let's get edit dir "a", and change it's name to primary

        # go into the root dirs page
        self.go_to_directories()
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

        self.assertEqual(self.directories_root_url, self.browser.current_url)
        self.assertInBody("primary")

    def test_list_documents(self):
        for i in range(10):
            DocumentFactory()
        # ensure that the table is loaded with data
        self.browser.get(self.custom_page_url + '#documents')
        WebDriverWait(self.browser, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME, "table"))
        )
        self.assertInBody('Showing 1 to 10 of 10 rows')

    def upload_check(self):
        before = len(Document.objects.all())
        upload_file = os.path.join(os.getcwd(), 'functional_tests/upload/test file.txt')
        self.assertTrue(os.path.exists(upload_file))

        file_input = self.browser.find_element_by_tag_name('input')
        file_input.send_keys(upload_file)
        self.browser.find_element_by_id('btn-upload').click()
        self.assertEqual(before + 1, len(Document.objects.all()))

    def test_upload_file(self):
        self.assertEqual(0, len(Document.objects.all()))
        self.browser.get(self.custom_page_url + '#documents/upload')
        WebDriverWait(self.browser, 2).until(
            EC.presence_of_element_located((By.ID, "btn-upload"))
        )
        self.upload_check()

    def test_upload_file_to_directory(self):
        init_test_dirs()
        # suppose there is already a lot of documents
        for i in range(10):
            PdfDocumentFactory()

        self.go_to_directories()
        self.enter_into_dir("a")
        self.browser.find_element_by_id('btn-upload-to-directory').click()
        self.upload_check()
        self.assertInBody('test file.txt')
