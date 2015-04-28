import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.six import BytesIO
from rest_framework.renderers import JSONRenderer
from django.test import TestCase
from rest_framework.parsers import JSONParser
from rest_framework.test import APIClient
from rest_framework import status

from cntapp.models import Directory, Document
from .helpers import init_test_dirs, PdfDocumentFactory, DirectoryFactory


class BaseRESTTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        PdfDocumentFactory.reset_sequence(force=True)

    def render(self, res):
        content = JSONRenderer().render(res.data)
        return JSONParser().parse(BytesIO(content))


class DocumentRESTTest(BaseRESTTest):
    def test_create_document(self):
        # good example
        file = SimpleUploadedFile('book.pdf', 'book content'.encode('utf-8'))
        res = self.client.post('/api/documents/', {'name': 'book.pdf', 'file': file})
        self.assertEqual(status.HTTP_201_CREATED, res.status_code)
        self.assertEqual({'id': 1,
                          'name': 'book.pdf',
                          'description': '',
                          'file': 'http://testserver/media/book.pdf',
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
        file = SimpleUploadedFile('book-1.pdf', 'book content'.encode('utf-8'))
        img_path = self.get_sample_file_path('cntapp/tests/images/wiki_logo_test.png')
        with open(img_path, 'rb') as thumbnail:
            res = self.client.post('/api/documents/', {'name': 'book-1.pdf', 'file': file, 'thumbnail': thumbnail})

        self.assertEqual(status.HTTP_201_CREATED, res.status_code)
        self.assertEqual({'id': 1,
                          'name': 'book-1.pdf',
                          'description': '',
                          'file': 'http://testserver/media/book-1.pdf',
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

    def test_get_document(self):
        PdfDocumentFactory.create(name="hello.pdf")
        res = self.client.get('/api/documents/1/')
        self.assertEqual(status.HTTP_200_OK, res.status_code)
        self.assertEqual({'id': 1,
                          'name': 'hello.pdf',
                          'description': '__description__0',
                          'file': 'http://testserver/media/hello.pdf',
                          'thumbnail': None},
                         self.render(res))

        # update document's name & description, & keep using the same file
        res = self.client.patch('/api/documents/1/',
                                {'name': 'not just hello.pdf', 'description': 'detailed description'})
        self.assertEqual({
                             'id': 1,
                             'name': 'not just hello.pdf',
                             'description': 'detailed description',
                             'file': 'http://testserver/media/hello.pdf',
                             'thumbnail': None
                         }, self.render(res))


class DirectoryRESTTest(BaseRESTTest):
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
        self.assertTrue(status.HTTP_200_OK, res.status_code)

        self.assertEqual(2, dir_a.get_sub_dirs().count())
        self.assertEqual({'status': 'sub directory created'},
                         self.render(res))

    def test_put_rename_dir(self):
        init_test_dirs()
        res = self.client.put('/api/directories/1/update/', {'name': 'Primary'}, format='json')
        self.assertEqual({'status': 'directory updated'}, self.render(res))
        d = Directory.objects.get(pk=1)
        self.assertEqual('Primary', d.name)

    def test_delete_sub_dir(self):
        init_test_dirs()
        ab_a = Directory.objects.get(name='ab_a')
        self.assertEqual(6, Directory.objects.all().count())

        res = self.client.delete('/api/directories/%d/delete/' % ab_a.pk, {'name': 'ab_a_a'}, format='json')
        self.assertEqual({'status': 'sub directory deleted'}, self.render(res))
        self.assertEqual(5, Directory.objects.all().count())

        res = self.client.delete('/api/directories/%d/delete/' % ab_a.pk, {'name': 'ab_a_b'}, format='json')
        self.assertEqual({'status': 'sub directory deleted'}, self.render(res))
        self.assertEqual(5, Directory.objects.all().count())

        with self.assertRaises(Directory.DoesNotExist):
            res = self.client.delete('/api/directories/%d/delete/' % ab_a.pk, {'name': 'ab_a_b'}, format='json')

    def test_delete_root_dir(self):
        init_test_dirs()
        a = Directory.objects.get(name='a')
        b = Directory.objects.get(name='b')
        self.assertEqual(6, Directory.objects.all().count())

        self.client.delete('/api/directories/%d/' % a.pk)
        self.assertEqual(5, Directory.objects.all().count())

        self.client.delete('/api/directories/%d/' % b.pk)
        self.assertEqual(2, Directory.objects.all().count())


class DirDocRelationRESTTest(BaseRESTTest):
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
                {'description': pdf_0.description,
                 'id': pdf_0.id,
                 'file': 'http://testserver' + pdf_0.file.url,
                 'name': pdf_0.name,
                 'thumbnail': None},
                {'description': pdf_1.description,
                 'id': pdf_1.id,
                 'file': 'http://testserver' + pdf_1.file.url,
                 'name': pdf_1.name,
                 'thumbnail': None},
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
