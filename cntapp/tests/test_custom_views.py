from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from cntapp.models import Directory
from cntapp.views.custom import index
from cntapp.helpers import get_root_dirs


class DirsCustomTestCase(TestCase):

    def test_index_only_show_root_dirs(self):
        response = index(HttpRequest())
        self.assertEqual(render_to_string('cntapp/custom/index.html'), response.content.decode())

        d0 = Directory(name='d0')
        d0.save()
        d1 = Directory(name='d1')
        d1.save()
        d2 = Directory(name='d2')
        d2.save()
        d1.add_sub_dir(d2)

        # index sees the directories that have no parent, so d2 is not visible
        context = {'dirs': [d0, d1]}
        response = index(HttpRequest())
        self.assertEqual(render_to_string('cntapp/custom/index.html', context), response.content.decode())

    def test_create_root_dir_on_index(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['new_dir_name'] = 'primary'
        self.assertEqual(0, Directory.objects.count())

        response = index(request)

        all_dirs = Directory.objects.all()
        self.assertEqual(1, all_dirs.count())
        self.assertEqual(render_to_string('cntapp/custom/index.html', {'dirs': all_dirs}),
                         response.content.decode())

    def test_create_dir_in_dir(self):
        self.client.post('/custom/', data={'new_dir_name': 'primary'})
        self.assertEqual(1, Directory.objects.count())
        self.client.post('/custom/primary/', data={'new_dir_name': 'CP'})
        self.assertEqual(2, Directory.objects.count())
        self.assertEqual(1, len(get_root_dirs()))
