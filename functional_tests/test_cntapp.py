from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from .base import FunctionalTest
from cntapp.tests.helpers import create_dir, PdfDocumentFactory


class FinalUserTest(FunctionalTest):

    def setUp(self):
        super().setUp()
        self.create_content()

    def create_content(self):
        """
Primary   -> CP
          -> CE1
          -> CE2
Secondary -> 3eme
          -> Second
          -> Terminal -> Math -> (Documents...)
        """
        primary = create_dir('Primary')
        secondary = create_dir('Secondary')

        cp = create_dir('CP')
        ce1 = create_dir('CE1')
        ce2 = create_dir('CE2')

        third_year = create_dir('3eme')
        second_year = create_dir('Second')
        final_year = create_dir('Terminal')
        math = create_dir('Math')

        primary.add_sub_dir(cp).add_sub_dir(ce1).add_sub_dir(ce2)
        secondary.add_sub_dir(third_year).add_sub_dir(second_year).add_sub_dir(final_year)
        final_year.add_sub_dir(math)

        for i in range(10):
            math.documents.add(PdfDocumentFactory())

    def go_to_home_page(self):
        self.browser.get(self.server_url)
        WebDriverWait(self.browser, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.navbar-brand'))
        )

    def go_into_directory(self, name):
        self.browser.find_element_by_link_text(name).click()

    def back_to_dir(self, name):
        state_bar = self.browser.find_element_by_class_name('navbar-lower')
        state_bar.find_element_by_link_text(name).click()

    def test_visit_index_page(self):
        self.go_to_home_page()
        self.assertInBody('Primary')
        self.assertInBody('Secondary')

    def test_navigate_directories(self):
        self.go_to_home_page()
        self.go_into_directory('Primary')
        self.assertInBody('CP')
        self.assertInBody('CE1')
        self.assertInBody('CE2')
        self.back_to_dir('Home')
        self.assertInBody('Primary')
        self.assertInBody('Secondary')

        # go into a directory that contains documents
        self.go_into_directory('Secondary')
        self.go_into_directory('Terminal')
        self.go_into_directory('Math')
        doc_list = self.browser.find_element_by_id('document-list')
        self.assertEqual(10, len(doc_list.find_elements_by_tag_name('li')))
