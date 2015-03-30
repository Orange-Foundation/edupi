from django.utils.six import BytesIO
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from django.test import TestCase
from rest_framework.parsers import JSONParser
from rest_framework.test import APIClient

from cntapp.models import Directory
from .helpers import init_test_dirs


class DirectoryRESTTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def render(self, res):
        content = JSONRenderer().render(res.data)
        return JSONParser().parse(BytesIO(content))

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
