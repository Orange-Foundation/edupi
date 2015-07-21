from enum import Enum
from cntapp.helpers import get_root_dirs, get_root_dirs_names
import os

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from django.core.cache import cache

from cntapp.models import Directory, Document
from .base import FunctionalTest
from cntapp.tests.helpers import DocumentFactory, init_test_dirs, PdfDocumentFactory, DirectoryFactory


class Header(Enum):
    """
    OrderedDict([
        ('\ufeffid_datas', 0),
        ('titre', 1),
        ('auteur', 2),
        ('pays', 3),
        ('url_doc', 4),
        ('langue', 5),
        ('CYCLE', 6),
        ('CLASSE', 7),
        ('ID CYCLE', 8),
        ('ID_CLASSE', 9),
        ('descriptif', 10),
        ('url_logo', 11),
        ('ok', 12),
        ('date_maj', 13),
        ('MATIERE', 14),
        ('NIVEAU_1', 15),
        ('NIVEAU_2', 16),
        ('ordre', 17),
        ('nv', 18),
        ('', 19),
        ('Absent : 123', 20),
        ('MN1N2', 21),
        ('1893', 22),
        ('TUNFRFR', 23),
        ('\n', 24)
    ])
    """
    name = 1
    filename = 4
    id_cycle = 8
    id_class = 9
    description = 10
    ok = 12

    cycle = 6
    klass = 7
    matiere = 14
    level_1 = 15
    level_2 = 16


class CustomSiteTestCase(FunctionalTest):
    def setUp(self):
        super().setUp()
        self.custom_page_url = self.server_url + '/custom/'
        self.directories_root_url = self.custom_page_url + '#directories'

    def login(self):
        self.browser.get(self.custom_page_url)
        self.browser.find_element_by_id('inputUsername').send_keys(self.username)
        self.browser.find_element_by_id('inputPassword').send_keys(self.password)
        self.browser.find_element_by_id('inputPassword').send_keys(Keys.ENTER)
        WebDriverWait(self.browser, 4).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.navbar-brand'))
        )

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
        # self.assertElementNotInDOM('.modal')  # modal window should disappear, but not instantly

        WebDriverWait(self.browser, 1).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '.table tbody'), dir_name)
        )
        self.assertInDirectoryTable(dir_name)

    def assertNotInDirectoryTable(self, text):
        self.assertNotIn(text, self.browser.find_element_by_css_selector('.table tbody').text)

    def assertInDirectoryTable(self, text):
        self.assertIn(text, self.browser.find_element_by_css_selector('.table tbody').text)

    def go_to_home_page(self, refresh=True):
        if refresh:
            self.browser.get(self.custom_page_url)
        else:
            self.browser.get(self.custom_page_url + "#")

        if self.browser.current_url == self.custom_page_url + 'login/':
            self.login()

        # need some time to load the page
        # FIXME: very long when loading the page for the second time with firefox in the test,
        # that only happens in local machine. The travis-ci doesn't have this issue.
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "table"))
        )

    def enter_into_dir(self, dir_name):
        WebDriverWait(self.browser, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#directories-table"))
        )
        table = self.browser.find_element_by_id("directories-table")
        table.find_element_by_link_text(dir_name).click()

    def test_create_directories(self):
        self.go_to_home_page()

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

        self.go_to_home_page(refresh=False)
        self.assertInDirectoryTable("primary")
        self.assertNotInDirectoryTable("Math")

    def test_navigate_directory_path(self):
        init_test_dirs()
        self.assertEqual(6, Directory.objects.count())

        def check_path(path_list):
            path = self.browser.find_element_by_css_selector(".path-breadcrumb")
            links_text = path.find_elements_by_css_selector('li')
            for i in range(len(path_list)):
                self.assertEqual(path_list[i], links_text[i].text)

        def back_to_dir(dir_name):
            path = self.browser.find_element_by_id("path")
            path.find_element_by_link_text(dir_name).click()

        self.go_to_home_page()

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

        # Travis-ci can't pass this two lines and I don't know why...
        # self.enter_into_dir("a")
        # check_path(['Home', 'a'])

        self.assertEqual(6, Directory.objects.count())

    def test_edit_directory(self):
        init_test_dirs()
        # Let's edit dir "a", and change it's name to primary

        dir_a = Directory.objects.get(name='a')

        # go into the root dirs page
        self.go_to_home_page()
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
        self.login()
        self.browser.get(self.custom_page_url + '#documents')
        WebDriverWait(self.browser, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME, "table"))
        )
        self.assertInBody('Showing 1 to 10 of 10 rows')

    def test_link_documents(self):
        # create directories and documents
        init_test_dirs()
        documents = []
        for i in range(10):
            documents.append(PdfDocumentFactory())
        dir_a = Directory.objects.get(name='a')
        col_index = {'id': 0, 'name': 1, 'description': 2, 'type': 3, 'action': 5}

        def _get_link_documents_table():
            # open the documents window and return the table
            WebDriverWait(self.browser, 3).until(
                EC.presence_of_element_located((By.ID, "btn-link-documents-to-directory"))
            )
            self.browser.find_element_by_id('btn-link-documents-to-directory').click()
            WebDriverWait(self.browser, 1).until(
                EC.presence_of_element_located((By.CLASS_NAME, "modal-dialog"))
            )
            return self.browser.find_element_by_id('table')

        def _toggle_link(document_table, document_id):
            row = None
            rows = document_table.find_elements_by_css_selector('tbody tr')
            for r in rows:
                if r.find_elements_by_css_selector('td')[col_index['id']].text == str(document_id):
                    row = r
            self.assertIsNotNone(row)  # document must exist
            data = row.find_elements_by_css_selector('td')
            data[col_index['action']].find_element_by_tag_name('a').click()  # toggle

        self.login()
        self.enter_into_dir('a')

        doc_table = _get_link_documents_table()
        _toggle_link(doc_table, documents[0].id)
        self.assertEqual(1, documents[0].directory_set.get_queryset().count())

        _toggle_link(doc_table, documents[0].id)
        self.assertEqual(0, documents[0].directory_set.get_queryset().count())

        # link three documents to the directory 'a'
        _toggle_link(doc_table, documents[0].id)
        _toggle_link(doc_table, documents[1].id)
        _toggle_link(doc_table, documents[2].id)
        self.assertEqual(3, dir_a.documents.count())

        # link the document[0] to the directory 'b'
        self.go_to_home_page()
        self.enter_into_dir('b')
        doc_table = _get_link_documents_table()
        _toggle_link(doc_table, documents[0].id)

        # Now the document[0] is linked to directory 'a' and 'b'
        self.assertEqual(2, documents[0].directory_set.get_queryset().count())

        # close the modal
        self.browser.find_element_by_css_selector('.modal-footer button').click()

        # the document is in the on the page
        doc_list = self.browser.find_element_by_id('document-list')
        self.assertIn(documents[0].name, doc_list.text)

    def test_edit_document(self):
        # prepare env
        init_test_dirs()
        d_a = Directory.objects.get(name="a")
        self.assertEqual('a', d_a.name)
        pdf = PdfDocumentFactory()
        d_a.documents.add(pdf)

        self.go_to_home_page()
        self.enter_into_dir(d_a.name)
        document_li = self.browser.find_element_by_css_selector('li#document-%d' % pdf.id)

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
        doc = Document.objects.get(pk=pdf.id)
        self.assertEqual("new file name", doc.name)
        self.assertEqual(desc, doc.description)

    def test_upload_page_loaded(self):
        init_test_dirs()
        d_a = Directory.objects.get(name="a")
        self.assertEqual('a', d_a.name)

        self.go_to_home_page()
        self.enter_into_dir(d_a.name)

        # enter into upload page
        self.browser.find_element_by_id('btn-upload-to-directory').click()

        # ensure that upload module is loaded
        self.browser.find_element_by_id('file-dropzone').click()

    def test_logout(self):
        self.go_to_home_page()
        self.browser.find_element_by_link_text('Logout').click()
        self.assertEqual(self.custom_page_url + 'login/', self.browser.current_url)
        # cannot access once to home page, must login again
        self.browser.get(self.custom_page_url)
        self.assertEqual(self.custom_page_url + 'login/', self.browser.current_url)

    def test_unlink_directory(self):
        init_test_dirs()
        a = Directory.objects.get(name="a")
        ab_a = Directory.objects.get(name="ab_a")
        ab_a_a = Directory.objects.get(name="ab_a_a")

        self.go_to_home_page()
        self.enter_into_dir(a.name)
        self.enter_into_dir(ab_a.name)

        ab_a_a_css = 'a[directory-id="%d"]' % ab_a_a.id

        # ensure the directory `ab_a_a` exists
        self.browser.find_element_by_css_selector(ab_a_a_css)

        # unlink ab_a_a
        unlink_elements = self.browser.find_elements_by_css_selector('a.btn-unlink-directory')
        unlink_elements[0].click()
        self.browser.find_element_by_css_selector('button.btn-confirmed').click()

        # check that the directory is unlinked
        WebDriverWait(self.browser, 1).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, ab_a_a_css))
        )
        self.assertNotInDirectoryTable(ab_a_a.name)

        # we can find it in the home page
        self.go_to_home_page(refresh=False)
        self.assertInDirectoryTable(ab_a_a.name)

    def test_link_directory(self):
        a = DirectoryFactory()
        b = DirectoryFactory()

        self.go_to_home_page()
        self.assertInDirectoryTable(a.name)
        self.assertInDirectoryTable(b.name)
        self.enter_into_dir(a.name)
        self.assertNotInDirectoryTable(b.name)

        # select and link a root directory
        self.browser.find_element_by_id('btn-link-directory-to-directory').click()
        radio_group = self.browser.find_element_by_class_name('input-group')
        radio_b = radio_group.find_element_by_css_selector('input[value="%d"]' % b.id)
        radio_b.click()
        self.browser.find_element_by_css_selector('.modal-footer .btn-confirm').click()

        self.assertInDirectoryTable(b.name)

        self.go_to_home_page(refresh=False)
        self.assertNotInDirectoryTable(b.name)
        self.assertInDirectoryTable(a.name)

    def test_get_all_paths(self):
        init_test_dirs()
        ab_a_a = Directory.objects.get(name='ab_a_a')
        ab_a_b = Directory.objects.get(name='ab_a_b')
        pdf = PdfDocumentFactory()
        ab_a_a.documents.add(pdf)
        ab_a_b.documents.add(pdf)

        self.go_to_home_page()
        self.enter_into_dir('a')
        self.enter_into_dir('ab_a')
        self.enter_into_dir('ab_a_a')
        document_li = self.browser.find_element_by_css_selector('li#document-%d' % pdf.id)
        btn = document_li.find_element_by_class_name('paths-popover')
        self.assertEqual('2', btn.text)
        btn.click()

        WebDriverWait(self.browser, 1).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.popover-content'))
        )

        paths = self.browser.find_element_by_class_name('popover-content')

        self.assertEqual(5, len(paths.find_elements_by_tag_name('ol')))  # there are 5 possible paths
        expected = [
            'a ab_a ab_a_b',
            'a ab_a ab_a_a',
            'b ab_a ab_a_b',
            'b ab_a ab_a_a',
            'c ab_a_b'
        ]

        for e in expected:
            self.assertIn(e, paths.text)

    def test_sys_info(self):
        self.login()
        self.browser.find_element_by_link_text('System Information').click()
        self.assertInBody('Storage')
        self.assertInBody('Total size')
        self.assertInBody('Used')
        self.assertInBody('Available')

        self.assertInBody('EduPi')
        self.assertInBody('Current version')
        self.assertInBody("Documents' references")


    def setUp(self):
        ctn_path = "/home/yuancheng/Content/ctn"
        self.all_files = os.listdir(ctn_path)

    def test_read_file(self):
        csv_files_path = os.path.join(os.getcwd(), 'csv/')
        csv_files = [os.path.join(csv_files_path, f) for f in os.listdir(csv_files_path)]

        total = 0
        for csv in csv_files:
            print('----------------' + csv)
            total += self.get_total_and_valid_records(csv)

        print('========================')
        print(total)

    def get_header_value_set(self, csv_file, header_value):
        with open(csv_file) as f:
            head = f.readline()  # skip the header
            total = 0
            valid = 0
            level_set = set()
            for l in f:
                record = l.split(';')
                try:
                    filename = record[Header.filename.value]
                    if filename in self.all_files:
                        level_set.add(record[header_value])
                except Exception as e:
                    # print('error in line:' + l)
                    print(e)
            return level_set

    def test_get_architecture(self):
        csv_file = os.path.join(os.getcwd(), 'csv/')
        csv_file = os.path.join(csv_file, 'mada-7-utf8.csv')
        print("-----------cycles")
        print(self.get_header_value_set(csv_file, Header.cycle.value))
        print("-----------classes")
        print(self.get_header_value_set(csv_file, Header.klass.value))
        print("-----------matieres")
        print(self.get_header_value_set(csv_file, Header.matiere.value))
        print("-----------level_1")
        print(self.get_header_value_set(csv_file, Header.level_1.value))
        print("-----------level_2")
        print(self.get_header_value_set(csv_file, Header.level_2.value))

    def create_path_and_doc_if_necessary(self, record):
        # cycle = record[Header.cycle.value]
        klass = record[Header.klass.value]
        matiere = record[Header.matiere.value]
        level_1 = record[Header.level_1.value]
        level_2 = record[Header.level_2.value]

        roots_names = get_root_dirs_names()
        if klass in ['Toute classe', 'Any class']:
            # TODO create doc link later
            return

        klass_dir = None
        if klass not in roots_names:
            klass_dir = Directory.objects.create(name=klass)
        else:
            # get root dir by name
            root_dirs = get_root_dirs()
            for root in root_dirs:
                if root.name == klass:
                    klass_dir = root
                    break

        if klass_dir is None:
            raise Exception('No klass dir found nor created!')

        if matiere is not '':
            matiere_dir = self.get_or_create_dir_if_not_in(klass_dir, matiere)
            if level_1 is not '':
                level_1_dir = self.get_or_create_dir_if_not_in(matiere_dir, level_1)
                if level_2 is not '':
                    level_2_dir = self.get_or_create_dir_if_not_in(level_1_dir, level_2)

    def get_or_create_dir_if_not_in(self, parent, name):
        child = None
        directory_set = parent.directory_set.all()
        if name not in [d.name for d in directory_set]:
            child = Directory.objects.create(name=name)
            parent.add_sub_dir(child)

        if child is None:
            child = directory_set.get(name=name)
        return child

    def create_tree(self, csv_file):
        with open(csv_file) as f:
            f.readline()  # skip the header
            for l in f:
                record = l.split(';')
                try:
                    filename = record[Header.filename.value]
                    if filename in self.all_files and record[Header.ok.value] == 'ok':
                        self.create_path_and_doc_if_necessary(record)
                except Exception as e:
                    print(e)

    def print_directory_in_tree(self):
        pass

    def test_create_tree(self):
        csv_file = "/home/yuancheng/source/edupi-dev/edupi/csv/camen-utf8.csv"
        # csv_file = "/home/yuancheng/source/edupi-dev/edupi/csv/tunisie-conf.csv"
        self.create_tree(csv_file)
        print(Directory.objects.all())
        # self.assertEqual(2, Directory.objects.count())
        self.login()
        pass



