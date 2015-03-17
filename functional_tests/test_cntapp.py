from django.test import LiveServerTestCase
from .base import FunctionalTest


class IndexPageTest(FunctionalTest):

    def test_visit_index_page(self):
        # enter into index page
        self.browser.get(self.server_url)

        # checkout the 'get started' link
        link = self.browser.find_element_by_id('id_get_started')
        self.assertEqual(link.get_attribute(name='href'), self.server_url + '/dirs/')

        link.click()

        # go to browse the directories
        self.assertEqual(self.browser.current_url, self.server_url + '/dirs/')
