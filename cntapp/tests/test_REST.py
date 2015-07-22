import os

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.six import BytesIO
from rest_framework.renderers import JSONRenderer
from django.test import TestCase
from rest_framework.parsers import JSONParser
from rest_framework.test import APIClient
from rest_framework import status

from cntapp.models import Directory, Document
from .helpers import init_test_dirs, PdfDocumentFactory, DirectoryFactory

User = get_user_model()


class BaseRESTTest(TestCase):
    def setUp(self):
        self.username = 'yuancheng'
        self.password = 'secret'
        self.user = User.objects.create_superuser(username=self.username, email='', password=self.password)
        self.client = APIClient()

        if not self.client.login(username=self.username, password=self.password):
            self.fail('Admin is not login')

        PdfDocumentFactory.reset_sequence(force=True)

    def render(self, res):
        content = JSONRenderer().render(res.data)
        return JSONParser().parse(BytesIO(content))


class DocumentRESTTest(BaseRESTTest):
    def test_without_authentication(self):
        self.client.logout()
        file = SimpleUploadedFile('book.txt', 'book content'.encode('utf-8'))
        res = self.client.post('/api/documents/', {'name': 'book.txt', 'file': file})
        self.assertEqual(status.HTTP_403_FORBIDDEN, res.status_code)
        self.assertEqual(status.HTTP_200_OK, self.client.get('/api/documents/').status_code)

    def test_create_document(self):
        # good example
        file = SimpleUploadedFile('book.txt', 'book content'.encode('utf-8'))
        res = self.client.post('/api/documents/', {'name': 'book.txt', 'file': file})
        self.assertEqual(status.HTTP_201_CREATED, res.status_code)
        self.assertEqual({'id': 1,
                          'name': 'book.txt',
                          'directory_set': [],
                          'description': '',
                          'file': 'http://testserver/media/book.txt',
                          'type': 'o',
                          'thumbnail': None},
                         self.render(res))

        # bad example
        res = self.client.post('/api/documents/', {})
        self.assertEqual(status.HTTP_400_BAD_REQUEST, res.status_code)
        self.assertEqual({'name': ['This field is required.'], 'file': ['No file was submitted.']},
                         self.render(res))

    def get_sample_file_path(self, path):
        return os.path.join(os.getcwd(), path)

    def test_create_document_with_thumbnail(self):
        file = SimpleUploadedFile('book-1.txt', 'book content'.encode('utf-8'))
        img_path = self.get_sample_file_path('cntapp/tests/images/wiki_logo_test.png')
        with open(img_path, 'rb') as thumbnail:
            res = self.client.post('/api/documents/', {'name': 'book-1.txt', 'file': file, 'thumbnail': thumbnail})

        self.assertEqual(status.HTTP_201_CREATED, res.status_code)
        self.assertEqual({'id': 1,
                          'name': 'book-1.txt',
                          'description': '',
                          'file': 'http://testserver/media/book-1.txt',
                          'type': 'o',
                          'directory_set': [],
                          'thumbnail': 'http://testserver/media/thumbnails/wiki_logo_test.png'},
                         self.render(res))

    def test_create_pdf_document_with_thumbnail(self):
        file_path = self.get_sample_file_path('cntapp/tests/samples/pdf-sample.pdf')
        with open(file_path, 'rb') as pdf:
            res = self.client.post('/api/documents/', {'name': pdf.name, 'file': pdf})
        self.assertEqual(status.HTTP_201_CREATED, res.status_code)
        json = self.render(res)
        self.assertEqual(json['id'], 1)
        self.assertEqual(json['name'], pdf.name)
        self.assertEqual(json['file'], 'http://testserver/media/pdf-sample.pdf')
        self.assertRegex(json['thumbnail'], r'tmp.+\.png')
        self.assertEqual(json['description'], '')
        self.assertEqual(json['type'], 'p')  # a real pdf

    def test_get_and_patch_document(self):
        PdfDocumentFactory.create(name="hello.pdf")
        res = self.client.get('/api/documents/1/')
        self.assertEqual(status.HTTP_200_OK, res.status_code)
        self.assertEqual({'id': 1,
                          'name': 'hello.pdf',
                          'description': '__description__0',
                          'file': 'http://testserver/media/hello.pdf',
                          'type': 'p',  # mocked pdf
                          'directory_set': [],
                          'thumbnail': None},
                         self.render(res))

        # update document's name & description, & keep using the same file
        res = self.client.patch('/api/documents/1/',
                                {'name': 'not just hello.pdf', 'description': 'detailed description'})
        self.assertEqual({'id': 1,
                          'name': 'not just hello.pdf',
                          'description': 'detailed description',
                          'file': 'http://testserver/media/hello.pdf',
                          'type': 'p',
                          'directory_set': [],
                          'thumbnail': None},
                         self.render(res))


class DirectoryRESTTest(BaseRESTTest):
    def test_without_authentication(self):
        self.client.logout()
        init_test_dirs()
        dir_a = Directory.objects.first()
        self.assertEqual(1, dir_a.get_sub_dirs().count())
        res = self.client.post('/api/directories/1/create_sub_directory/', {'name': 'Primary'}, format='json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, res.status_code)
        self.assertEqual(status.HTTP_200_OK, self.client.get('/api/directories/').status_code)

    def test_get_dir(self):
        init_test_dirs()
        res = self.client.get('/api/directories/1/')
        self.assertEqual({'id': 1, 'url': 'http://testserver/api/directories/1/', 'name': 'a'},
                         self.render(res))

    def test_get_root_dirs(self):
        init_test_dirs()
        res = self.client.get('/api/directories/?root=true')
        self.assertEqual([{'id': 1, 'name': 'a', 'url': 'http://testserver/api/directories/1/'},
                          {'id': 2, 'name': 'b', 'url': 'http://testserver/api/directories/2/'},
                          {'id': 3, 'name': 'c', 'url': 'http://testserver/api/directories/3/'}],
                         self.render(res))

    def test_get_sub_dirs(self):
        init_test_dirs()

        res = self.client.get('/api/directories/1/sub_directories/')
        self.assertEqual([{'id': 4, 'url': 'http://testserver/api/directories/4/', 'name': 'ab_a'}],
                         self.render(res))

        res = self.client.get('/api/directories/4/sub_directories/')
        self.assertEqual([{'id': 5, 'url': 'http://testserver/api/directories/5/', 'name': 'ab_a_a'},
                          {'id': 6, 'url': 'http://testserver/api/directories/6/', 'name': 'ab_a_b'}],
                         self.render(res))

    def test_post_create_root_dir(self):
        res = self.client.post('/api/directories/', {'name': 'Primary'}, format='json')
        self.assertEqual({'id': 1, 'url': 'http://testserver/api/directories/1/', 'name': 'Primary'},
                         self.render(res))
        d = Directory.objects.first()
        self.assertEqual('Primary', d.name)

    def test_post_create_sub_directory(self):
        init_test_dirs()
        dir_a = Directory.objects.first()
        self.assertEqual(1, dir_a.get_sub_dirs().count())

        res = self.client.post('/api/directories/1/create_sub_directory/', {'name': 'Primary'}, format='json')
        self.assertEqual(status.HTTP_200_OK, res.status_code)

        self.assertEqual(2, dir_a.get_sub_dirs().count())
        self.assertEqual({'status': 'sub directory created'},
                         self.render(res))

    def test_put_rename_dir(self):
        init_test_dirs()
        res = self.client.patch('/api/directories/1/', {'name': 'Primary'}, format='json')
        self.assertEqual({'id': 1, 'name': 'Primary', 'url': 'http://testserver/api/directories/1/'},
                         self.render(res))
        d = Directory.objects.get(pk=1)
        self.assertEqual('Primary', d.name)

    def test_delete_sub_dir(self):
        init_test_dirs()
        ab_a = Directory.objects.get(name='ab_a')
        ab_a_a = Directory.objects.get(name='ab_a_a')
        ab_a_b = Directory.objects.get(name='ab_a_b')
        self.assertEqual(6, Directory.objects.all().count())

        res = self.client.delete('/api/directories/%d/delete/' % ab_a.pk, {'id': ab_a_a.pk}, format='json')
        self.assertEqual({'status': 'sub directory deleted'}, self.render(res))
        self.assertEqual(5, Directory.objects.all().count())

        res = self.client.delete('/api/directories/%d/delete/' % ab_a.pk, {'id': ab_a_b.pk}, format='json')
        self.assertEqual({'status': 'sub directory deleted'}, self.render(res))
        self.assertEqual(5, Directory.objects.all().count())

    def test_delete_root_dir(self):
        init_test_dirs()
        a = Directory.objects.get(name='a')
        b = Directory.objects.get(name='b')
        self.assertEqual(6, Directory.objects.all().count())

        self.client.delete('/api/directories/%d/' % a.pk)
        self.assertEqual(5, Directory.objects.all().count())

        self.client.delete('/api/directories/%d/' % b.pk)
        self.assertEqual(2, Directory.objects.all().count())

    def test_unlink_dir(self):
        init_test_dirs()
        ab_a = Directory.objects.get(name='ab_a')
        ab_a_a = Directory.objects.get(name='ab_a_a')
        self.assertEqual(6, Directory.objects.all().count())
        res = self.client.delete('/api/directories/%d/directories/' % ab_a.pk, {'id': str(ab_a_a.pk)}, format='json')
        self.assertEqual(status.HTTP_200_OK, res.status_code)
        self.assertEqual({'status': 'sub directory unlinked'}, self.render(res))
        self.assertEqual(6, Directory.objects.all().count())

        # delete again
        res = self.client.delete('/api/directories/%d/directories/' % ab_a.pk, {'id': str(ab_a_a.pk)}, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, res.status_code)
        self.assertEqual({'status': 'Relation does not exist'}, self.render(res))

    def test_link_dir(self):
        a = DirectoryFactory()
        b = DirectoryFactory()
        res = self.client.post('/api/directories/%d/directories/' % a.pk, {'id': str(b.pk)}, format='json')
        self.assertEqual(status.HTTP_201_CREATED, res.status_code)
        self.assertIn(b, a.get_sub_dirs())
        self.assertEqual({'status': 'relation created'}, self.render(res))

        # link again
        res = self.client.post('/api/directories/%d/directories/' % a.pk, {'id': str(b.pk)}, format='json')
        self.assertIn(b, a.get_sub_dirs())
        self.assertEqual({'status': 'relation created'}, self.render(res))

    def test_link_dir_incorrectly(self):
        a = DirectoryFactory()
        b = DirectoryFactory()
        res = self.client.post('/api/directories/%d/directories/' % a.pk, {'i': str(b.pk)}, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, res.status_code)
        self.assertEqual({'status': 'no sub-directory id is provided'}, self.render(res))

    def test_unlink_dir_incorrectly(self):
        init_test_dirs()
        ab_a = Directory.objects.get(name='ab_a')
        ab_a_a = Directory.objects.get(name='ab_a_a')
        self.assertEqual(6, Directory.objects.all().count())
        # no `id` in the request
        res = self.client.delete('/api/directories/%d/directories/' % ab_a.pk, {'i': str(ab_a_a.pk)}, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, res.status_code)
        self.assertEqual({'status': 'no sub-directory id is provided'}, self.render(res))

        # sub directory does not exist
        res = self.client.delete('/api/directories/%d/directories/' % ab_a.pk, {'id': '999'}, format='json')
        self.assertEqual(status.HTTP_404_NOT_FOUND, res.status_code)
        self.assertEqual({'detail': 'Not found.'}, self.render(res))

        # delete it-self
        res = self.client.delete('/api/directories/%d/directories/' % ab_a.pk, {'id': str(ab_a.pk)}, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, res.status_code)
        self.assertEqual({'status': 'Relation does not exist'}, self.render(res))
        self.assertEqual(6, Directory.objects.all().count())

    def test_get_paths(self):
        init_test_dirs()
        a = Directory.objects.get(name='a')
        ab_a_b = Directory.objects.get(name='ab_a_b')
        res = self.client.get('/api/directories/%d/paths/' % a.pk)
        self.assertEqual(status.HTTP_200_OK, res.status_code)
        self.assertEqual([
            [
                {'id': 1, 'url': 'http://testserver/api/directories/1/', 'name': 'a'}
            ]
        ],
            self.render(res))

        res = self.client.get('/api/directories/%d/paths/' % ab_a_b.pk)
        self.assertEqual(status.HTTP_200_OK, res.status_code)
        self.assertEqual([
            [
                {'url': 'http://testserver/api/directories/1/', 'id': 1, 'name': 'a'},
                {'url': 'http://testserver/api/directories/4/', 'id': 4, 'name': 'ab_a'},
                {'url': 'http://testserver/api/directories/6/', 'id': 6, 'name': 'ab_a_b'}
            ], [
                {'url': 'http://testserver/api/directories/2/', 'id': 2, 'name': 'b'},
                {'url': 'http://testserver/api/directories/4/', 'id': 4, 'name': 'ab_a'},
                {'url': 'http://testserver/api/directories/6/', 'id': 6, 'name': 'ab_a_b'}
            ], [
                {'url': 'http://testserver/api/directories/3/', 'id': 3, 'name': 'c'},
                {'url': 'http://testserver/api/directories/6/', 'id': 6, 'name': 'ab_a_b'}
            ]
        ],
            self.render(res))


class DirDocRelationRESTTest(BaseRESTTest):

    def test_get_dir_sub_content(self):
        d = DirectoryFactory()
        d1 = DirectoryFactory()
        doc1 = PdfDocumentFactory()

        d.add_sub_dir(d1)
        d.documents.add(doc1)

        res = self.client.get('/api/directories/%d/sub_content/' % d.pk)
        self.assertEqual({
            'directories': [
                {
                    'url': 'http://testserver/api/directories/2/', 'name': d1.name, 'id': d1.id
                }
            ],
            'documents': [
                {
                    'name': doc1.name, 'id': doc1.pk,
                    'file': 'http://testserver' + doc1.file.url,
                    'type': 'p', 'thumbnail': None,
                    'description': doc1.description,
                    'directory_set': [
                        {
                            'url': 'http://testserver/api/directories/%d/' % d.id, 'name': d.name,
                            'id': d.pk
                        }
                    ]
                }
            ]
        }, self.render(res))
        pass

    def test_get_documents_from_directory(self):
        d = DirectoryFactory()
        # empty directory
        res = self.client.get('/api/directories/%d/documents/' % d.pk)
        self.assertEqual([], self.render(res))

        pdf_0 = PdfDocumentFactory()
        pdf_1 = PdfDocumentFactory()
        d.documents.add(pdf_0)
        d.documents.add(pdf_1)
        self.assertEqual(2, len(d.documents.all()))

        res = self.client.get('/api/directories/%d/documents/' % d.pk)
        self.assertEqual(
            [
                {
                    'description': pdf_0.description,
                    'id': pdf_0.id,
                    'file': 'http://testserver' + pdf_0.file.url,
                    'name': pdf_0.name,
                    'type': 'p',
                    'thumbnail': None,
                    'directory_set': [
                        {
                            'name': d.name, 'url': 'http://testserver/api/directories/%d/' % d.id, 'id': d.id
                        }
                    ],
                },
                {
                    'description': pdf_1.description,
                    'id': pdf_1.id,
                    'file': 'http://testserver' + pdf_1.file.url,
                    'name': pdf_1.name,
                    'type': 'p',
                    'thumbnail': None,
                    'directory_set': [
                        {
                            'name': d.name, 'url': 'http://testserver/api/directories/%d/' % d.id, 'id': d.id
                        }
                    ],
                },
            ],
            self.render(res))

    def test_add_document_to_directory(self):
        d = DirectoryFactory()
        pdf = PdfDocumentFactory()
        res = self.client.post('/api/directories/%d/documents/' % d.pk)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, res.status_code)
        self.assertEqual({'documents': 'This field should contain a list of document id'},
                         self.render(res))

        # add a single document
        res = self.client.post('/api/directories/%d/documents/' % d.pk, data={'documents': [pdf.pk]}, format='json')
        self.assertEqual(status.HTTP_201_CREATED, res.status_code)
        self.assertEqual(pdf, d.documents.first())

    def test_add_documents_to_directory(self):
        # add a list of documents
        d = DirectoryFactory()
        pdf_0 = PdfDocumentFactory()
        pdf_1 = PdfDocumentFactory()

        res = self.client.post('/api/directories/%d/documents/' % d.pk,
                               data={'documents': [pdf_0.id, pdf_1.id]}, format='json')
        self.assertEqual(status.HTTP_201_CREATED, res.status_code)
        d = Directory.objects.get(pk=d.pk)
        self.assertEqual(2, d.documents.count())
        self.assertEqual(pdf_0, d.documents.get(pk=pdf_0.pk))
        self.assertEqual(pdf_1, d.documents.get(pk=pdf_1.pk))

    def test_add_not_exist_documents_to_directory(self):
        d = DirectoryFactory()
        pdf_0 = PdfDocumentFactory()
        res = self.client.post('/api/directories/%d/documents/' % d.pk,
                               data={'documents': [pdf_0.id, '100']}, format='json')
        self.assertEqual(status.HTTP_404_NOT_FOUND, res.status_code)
        self.assertEqual(0, d.documents.count())

    def test_remove_documents_from_directory(self):
        d = DirectoryFactory()
        pdf_0 = PdfDocumentFactory()
        pdf_1 = PdfDocumentFactory()
        pdf_2 = PdfDocumentFactory()
        pdf_3 = PdfDocumentFactory()
        d.documents.add(pdf_0)
        d.documents.add(pdf_1)
        d.documents.add(pdf_2)
        d.documents.add(pdf_3)

        res = self.client.delete('/api/directories/%d/documents/' % d.pk)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, res.status_code)

        res = self.client.delete('/api/directories/%d/documents/' % d.pk,
                                 data={'documents': [pdf_0.id]}, format='json')
        self.assertEqual(status.HTTP_200_OK, res.status_code)
        self.assertEqual(3, d.documents.count())

        res = self.client.delete('/api/directories/%d/documents/' % d.pk,
                                 data={'documents': [pdf_0.id, pdf_1.id]}, format='json')
        self.assertEqual(status.HTTP_404_NOT_FOUND, res.status_code)
        self.assertEqual(3, d.documents.count())

        res = self.client.delete('/api/directories/%d/documents/' % d.pk,
                                 data={'documents': [pdf_1.id, pdf_2.id]}, format='json')
        self.assertEqual(1, d.documents.count())
        self.assertEqual(4, Document.objects.count())
