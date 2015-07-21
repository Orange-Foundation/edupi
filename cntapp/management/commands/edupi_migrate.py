import unittest
from django.test import TestCase
import os

from django.core.management.base import NoArgsCommand, AppCommand
from django.contrib.auth import get_user_model
from django.utils.six import BytesIO
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from rest_framework.test import APIClient
from rest_framework import status

from .header import Header
from functional_tests.base import FunctionalTest
from cntapp.models import Directory, Document
from cntapp.helpers import get_root_dirs, get_root_dirs_names
from .klasses import klasses

User = get_user_model()


class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        suite = unittest.TestLoader().loadTestsFromTestCase(MigrationTest, )
        unittest.TextTestRunner().run(suite)


class MigrationTest(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.ctn_path = "/home/yuancheng/Content/ctn"
        self.all_files = os.listdir(self.ctn_path)
        # TODO
        self.klasses = klasses['cmen']

        self.username = 'pi'
        self.password = 'raspberry'
        # self.user = User.objects.create_superuser(username=self.username, email='', password=self.password)
        self.client = APIClient()

        if not self.client.login(username=self.username, password=self.password):
            self.fail('Admin is not login')

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
        self.upload_file_if_not_exist(record)

        klass = record[Header.klass.value]
        roots_names = get_root_dirs_names()
        if klass in ['Toute classe', 'Any class']:
            for kls_dir in get_root_dirs():
                self._create_dirs_for_klass(record, kls_dir)
            return

        if klass not in self.klasses:
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
        roots = get_root_dirs_names()
        for root in self.klasses:
            if root not in roots:
                Directory.objects.create(name=root)

    def render(self, res):
        content = JSONRenderer().render(res.data)
        return JSONParser().parse(BytesIO(content))

    def upload_file_if_not_exist(self, record):
        if not Document.objects.filter(file='./' + record[Header.filename.value]).exists():
            file = os.path.join(self.ctn_path, record[Header.filename.value])
            with open(file, 'rb') as f:
                res = self.client.post('/api/documents/', {'name': record[Header.name.value], 'file': f})

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
        print("get file:" + filename)
        d = Document.objects.get(file=filename)

        res = self.client.post(
            '/api/directories/%d/documents/' % final_dir.pk, data={'documents': [d.pk]}, format='json')
        self.assertEqual(status.HTTP_201_CREATED, res.status_code)

    def _link_doc(self, record):
        klass = record[Header.klass.value]
        if klass in ['Toute classe', 'Any class']:
            for kls in self.klasses:
                self.__link_doc(record, kls)
        elif klass not in self.klasses:
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
        csv_file = "/home/yuancheng/source/edupi-dev/edupi/csv/camen-utf8.csv"
        # csv_file = "/home/yuancheng/source/edupi-dev/edupi/csv/camfr-utf8.csv"
        self.create_basic_tree()
        self.create_tree(csv_file)
        self.link_docs(csv_file)
        print(Directory.objects.all())
        print(Directory.objects.count())
        print(Document.objects.count())
        # self.login()
        # pass
