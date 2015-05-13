import os

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

from cntapp.models import Directory, Document
from .base import FunctionalTest
from cntapp.tests.helpers import DocumentFactory, init_test_dirs, PdfDocumentFactory


class CustomSiteTestCase(FunctionalTest):

    def setUp(self):
        super().setUp()
        self.custom_page_url = self.server_url + '/custom/'
        self.directories_root_url = self.custom_page_url + '#directories'

    def assertElementNotInDOM(self, css_selector):
        try:
            self.browser.find_element_by_css_selector(css_selector)
            self.fail()
        except NoSuchElementException:
            pass

    def create_dir(self, dir_name):
        self.assertNotInBody(dir_name)

        # click create directory button to show a modal window
        actions = ActionChains(self.browser)
        actions.move_to_element(self.browser.find_element_by_id('create-directory'))
        actions.click()
        actions.perform()
        WebDriverWait(self.browser, 1).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.modal'))
        )

        # create directory in a modal window
        name_input = self.browser.find_element_by_id('input-directory-name')
        name_input.click()
        name_input.send_keys(dir_name)
        name_input.send_keys(Keys.ENTER)
        self.assertElementNotInDOM('.modal')

        WebDriverWait(self.browser, 1).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '.table tbody'), dir_name)
        )
        self.assertInDirectoryTable(dir_name)

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
        self.go_to_directories()

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
            pe = self.browser.find_element_by_css_selector("div#path ul")
            links_text = pe.find_elements_by_css_selector('li')
            for i in range(len(path_list)):
                self.assertEqual(path_list[i], links_text[i].text)

        def back_to_dir(dir_name):
            path = self.browser.find_element_by_id("path")
            path.find_element_by_link_text(dir_name).click()

        self.go_to_directories()

        self.enter_into_dir("a")
        check_path(['Home', 'a'])
        self.enter_into_dir("ab_a")
        check_path(['Home', 'a', 'ab_a'])
        self.enter_into_dir("ab_a_a")
        check_path(['Home', 'a', 'ab_a', 'ab_a_a'])

        self.browser.refresh()
        WebDriverWait(self.browser, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME, "table"))
        )

        check_path(['Home', 'a', 'ab_a', 'ab_a_a'])

        back_to_dir("ab_a")
        check_path(['Home', 'a', 'ab_a'])
        back_to_dir("a")
        check_path(['Home', 'a'])
        back_to_dir("Home")
        self.enter_into_dir("a")
        check_path(['Home', 'a'])
        self.assertEqual(6, Directory.objects.count())

    def test_edit_directory(self):
        init_test_dirs()
        ## Let's get edit dir "a", and change it's name to primary

        dir_a = Directory.objects.get(name='a')

        # go into the root dirs page
        self.go_to_directories()
        new_name = 'primary'
        self.assertNotEqual(new_name, dir_a.name)
        self.assertNotInBody(new_name)

        edit_elements = self.browser.find_elements_by_css_selector('a.btn-edit')
        self.assertEqual(3, len(edit_elements))

        # edit_dir_a = edit_elements[0]
        edit_dir_a = self.browser.find_element_by_css_selector(
            'a[data-target="#modal-directory-edit-%d"]' % dir_a.id)
        edit_dir_a.click()

        WebDriverWait(self.browser, 1).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.modal'))
        )

        # change the name
        name_input = self.browser.find_element_by_id('input-directory-name')
        name_input.click()
        name_input.clear()
        name_input.send_keys(new_name)
        self.browser.find_element_by_css_selector('button.btn-edit-confirm').click()

        # ensure there is no more modal
        self.assertElementNotInDOM('.modal')

        self.assertEqual(self.directories_root_url, self.browser.current_url)
        self.assertInDirectoryTable(new_name)

        # check in server side
        self.assertEqual(new_name, Directory.objects.get(id=dir_a.id).name)

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

    def test_edit_document(self):
        # prepare env
        init_test_dirs()
        d_a = Directory.objects.get(name="a")
        self.assertEqual('a', d_a.name)
        pdf = PdfDocumentFactory()
        d_a.documents.add(pdf)

        self.go_to_directories()
        self.enter_into_dir(d_a.name)
        document_li = self.browser.find_element_by_css_selector('li#document-1')

        # hover on the document item
        actions = ActionChains(self.browser)
        actions.move_to_element(document_li)
        actions.move_to_element(document_li.find_element_by_css_selector(".glyphicon-pencil"))
        actions.click()
        actions.perform()

        # clear the name and try to save it
        name_input = document_li.find_element_by_css_selector("input[name='name']")
        name_input.clear()
        document_li.find_element_by_css_selector(".btn-save").click()
        self.assertInBody('name must not be empty')

        # enter a new name
        name_input.send_keys("new file name")
        # enter a Description
        desc = "this is a good description for the file"
        desc_input = document_li.find_element_by_css_selector("textarea[name='description']")
        desc_input.clear()
        desc_input.send_keys(desc)

        document_li.find_element_by_css_selector(".btn-save").click()

        self.assertInBody('new file name')
        self.assertInBody(desc)
        doc = Document.objects.get(pk=1)
        self.assertEqual("new file name", doc.name)
        self.assertEqual(desc, doc.description)
