from django.template.loader import render_to_string

from django.test import TestCase
from django.http import HttpRequest
from django.core.urlresolvers import resolve
from django.core.urlresolvers import Resolver404

from cntapp.views.custom import index, resolve_dirs_structure
from cntapp.models import Directory
from cntapp.tests.helpers import create_dir, init_test_dirs
from cntapp.helpers import get_root_dirs, get_dir_by_path


class DirsCustomTestCase(TestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_index_url_resolve(self):
        found = resolve('/custom/')
        self.assertEqual(found.func, index)

    def check_index_html(self, request, context=None):
        response = index(request)
        self.assertEqual(render_to_string('cntapp/custom/index.html', context), response.content.decode())
        return response

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

    def test_enter_into_dirs(self):
        init_test_dirs()
        response = self.check_index_html(HttpRequest(), context={'dirs': get_root_dirs()})
        self.fail('please finish this test!')

    def test_levels_url_resolve(self):
        init_test_dirs()
        urls = ['/custom/a/', '/custom/a_a/', '/custom/a/a_a_a/']
        map(self.assertEqual, zip([resolve(u).func for u in urls], [resolve_dirs_structure] * len(urls)))

    def test_get_url_by_path(self):
        init_test_dirs()
        d = get_dir_by_path('a/ab_a/ab_a_a')
        self.assertEqual('ab_a_a', d.name)
