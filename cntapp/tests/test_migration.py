from django.contrib.auth import get_user_model
from django.utils.six import BytesIO
from rest_framework.renderers import JSONRenderer
from django.test import TestCase
from rest_framework.parsers import JSONParser

from functional_tests.base import FunctionalTest

User = get_user_model()

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from enum import Enum
from selenium.webdriver.support.ui import WebDriverWait
import os

from django.core.files.uploadedfile import SimpleUploadedFile, File
from rest_framework.test import APIClient
from rest_framework import status

from cntapp.models import Directory, Document

from cntapp.helpers import get_root_dirs, get_root_dirs_names


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


class MigrationTest(FunctionalTest):
    def setUp(self):
        super().setUp()
        self.ctn_path = "/home/yuancheng/Content/ctn"
        self.all_files = os.listdir(self.ctn_path)
        self.custom_page_url = self.server_url + '/custom/'
        self.directories_root_url = self.custom_page_url + '#directories'
        self.tn_primary_klasses = [
            'tn - 1ère année',
            'tn - 2ème année',
            'tn - 3ème année',
            'tn - 4ème année',
            'tn - 5ème année',
            'tn - 6ème année',
        ]

        self.username = 'yuancheng_1'
        self.password = 'secret'
        self.user = User.objects.create_superuser(username=self.username, email='', password=self.password)
        self.client = APIClient()

        if not self.client.login(username=self.username, password=self.password):
            self.fail('Admin is not login')


    def login(self):
        self.browser.get(self.custom_page_url)
        self.browser.find_element_by_id('inputUsername').send_keys(self.username)
        self.browser.find_element_by_id('inputPassword').send_keys(self.password)
        self.browser.find_element_by_id('inputPassword').send_keys(Keys.ENTER)
        WebDriverWait(self.browser, 4).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.navbar-brand'))
        )

    def test_enum(self):
        print(Header.name.value)

    def get_total_and_valid_records(self, csv_file):
        with open(csv_file) as f:
            f.readline()  # skip the header
            total = 0
            valid = 0
            sum_ok = 0
            for l in f:
                # l = f.readline()
                total += 1
                record = l.split(';')
                try:
                    filename = record[Header.filename.value]
                    if filename in self.all_files:
                        valid += 1
                    if record[Header.ok.value] == 'ok':
                        sum_ok += 1
                except Exception as e:
                    print('error in line:' + l)
                    print(e)

            print(total)
            print(valid)
            print(sum_ok)

        return total

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
        csv_file = os.path.join(csv_file, 'senegal_1410_09h45-2-utf8.csv')
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

    def _create_dirs_for_klass(self, record, klass_dir):
        matiere = record[Header.matiere.value]
        level_1 = record[Header.level_1.value]
        level_2 = record[Header.level_2.value]
        if matiere is not '':
            matiere_dir = self.get_or_create_dir_if_not_in(klass_dir, matiere)
            if level_1 is not '':
                level_1_dir = self.get_or_create_dir_if_not_in(matiere_dir, level_1)
                if level_2 is not '':
                    level_2_dir = self.get_or_create_dir_if_not_in(level_1_dir, level_2)

    def create_path_and_doc_if_necessary(self, record):
        ### upload file
        # TODO: do not upload the same file
        self.upload_file(record)

        klass = record[Header.klass.value]
        roots_names = get_root_dirs_names()
        if klass in ['Toute classe', 'Any class']:
            for kls_dir in get_root_dirs():
                self._create_dirs_for_klass(record, kls_dir)
            return

        if klass not in self.tn_primary_klasses:
            return

        klass_dir = None
        if klass not in roots_names:
            klass_dir = Directory.objects.create(name=klass)
        else:
            # get root dir by name
            root_dirs = get_root_dirs()
            klass_dir = [root for root in root_dirs if root.name == klass][0]

        self._create_dirs_for_klass(record, klass_dir)



    def get_or_create_dir_if_not_in(self, parent, name):
        child = None

        try:
            child = parent.get_sub_dir_by_name(name)
        except Directory.DoesNotExist as e:
            child = Directory.objects.create(name=name)
            parent.add_sub_dir(child)
        finally:
            if child is None:
                raise Exception('unexpected error when getting child:' + name)
            return child

    def create_tree(self, csv_file):
        with open(csv_file) as f:
            f.readline()  # skip the header
            parsed_total = 0
            for l in f:
                record = l.split(';')
                try:
                    filename = record[Header.filename.value]
                    if filename in self.all_files and record[Header.ok.value] == 'ok':
                        self.create_path_and_doc_if_necessary(record)
                        parsed_total += 1
                        print(parsed_total)
                except Exception as e:
                    print(e)

    def create_basic_tree(self):
        for root in self.tn_primary_klasses:
            Directory.objects.create(name=root)

    def render(self, res):
        content = JSONRenderer().render(res.data)
        return JSONParser().parse(BytesIO(content))

    def upload_file(self, record):
        file = os.path.join(self.ctn_path, record[Header.filename.value])
        with open(file, 'rb') as f:
            res = self.client.post('/api/documents/', {'name': record[Header.name.value], 'file': f})

    def test_upload_files(self):
        csv_file = "/home/yuancheng/source/edupi-dev/edupi/csv/tn-reduced.csv"

    def test_create_document(self):
        # good example
        # file = SimpleUploadedFile('book.txt', 'book content'.encode('utf-8'))
        file = os.path.join(os.getcwd(), 'functional_tests/upload/test file.txt')
        with open(file, 'rb') as f:
            res = self.client.post('/api/documents/', {'name': 'book.txt', 'file': f})
        self.assertEqual(status.HTTP_201_CREATED, res.status_code)
        self.assertEqual({'id': 1,
                          'name': 'book.txt',
                          'directory_set': [],
                          'description': '',
                          'file': 'http://testserver/media/book.txt',
                          'type': 'o',
                          'thumbnail': None}, self.render(res))

    def __link_doc(self, record, kls):
        matiere = record[Header.matiere.value]
        level_1 = record[Header.level_1.value]
        level_2 = record[Header.level_2.value]

        root_dir = [r for r in get_root_dirs() if r.name == kls][0]
        final_dir = root_dir

        if matiere is not '':
            final_dir = root_dir.get_sub_dir_by_name(matiere)
            if level_1 is not '':
                final_dir = final_dir.get_sub_dir_by_name(level_1)
                if level_2 is not '':
                    final_dir = final_dir.get_sub_dir_by_name(level_2)

        # link document to final dir
        filename = './' + record[Header.filename.value]
        d = Document.objects.get(file=filename)

        res = self.client.post(
            '/api/directories/%d/documents/' % final_dir.pk, data={'documents': [d.pk]}, format='json')
        self.assertEqual(status.HTTP_201_CREATED, res.status_code)

    def _link_doc(self, record):
        klass = record[Header.klass.value]
        if klass in ['Toute classe', 'Any class']:
            for kls in self.tn_primary_klasses:
                self.__link_doc(record, kls)
        elif klass not in self.tn_primary_klasses:
            return
        else:
            self.__link_doc(record, klass)

    def link_docs(self, csv_file):
        with open(csv_file) as f:
            f.readline()  # skip the header
            total = 0
            for l in f:
                record = l.split(';')
                try:
                    filename = record[Header.filename.value]
                    if filename in self.all_files and record[Header.ok.value] == 'ok':
                        self._link_doc(record)
                        total += 1
                        print('linking doc: %d' % total)
                except Exception as e:
                    print(e)

    def test_create_tree(self):
        # csv_file = "/home/yuancheng/source/edupi-dev/edupi/csv/camen-utf8.csv"
        csv_file = "/home/yuancheng/source/edupi-dev/edupi/csv/tn-reduced.csv"
        self.create_basic_tree()
        self.create_tree(csv_file)
        self.link_docs(csv_file)
        print(Directory.objects.all())
        print(Directory.objects.count())
        self.login()
        pass




