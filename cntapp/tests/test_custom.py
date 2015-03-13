from django.template.loader import render_to_string
from django.test import TestCase
from django.http import HttpRequest
from django.core.urlresolvers import resolve

from cntapp.views.custom import index
from cntapp.models import Directory


class DirsCustomTestCase(TestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_index_url_resolve(self):
        found = resolve('/custom/')
        self.assertEqual(found.func, index)

    def test_create_dir(self):
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

    def test_create_dir_by_POST(self):
        self.assertEqual(render_to_string('cntapp/custom/index.html'), index(HttpRequest()).content.decode())

        request = HttpRequest()
        request.method = 'POST'
        request.POST['new_dir_name'] = 'primary'

        response = index(request)

        all_dirs = Directory.objects.all()
        self.assertEqual(1, all_dirs.count())
        self.assertEqual(render_to_string('cntapp/custom/index.html', {'dirs': all_dirs}),
                         response.content.decode())
