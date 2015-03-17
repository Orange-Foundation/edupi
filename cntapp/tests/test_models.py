from django.test import TestCase
from django.db.models import ObjectDoesNotExist

from cntapp.models import Directory, Document, SubDirRelation


class DocumentTest(TestCase):
    def setUp(self):
        pass

    def test_create_document(self):
        Document.objects.create(
            name='manual', type=Document.TYPE_PDF, description='this is a pdf')
        d = Document.objects.get(name='manual')
        self.assertEqual(d.type, Document.TYPE_PDF)


class DirectoryTestCase(TestCase):
    def setUp(self):
        pass

    def create_dir(self, dir_name):
        d = Directory(name=dir_name)
        d.save()
        return d

    def test_create_dir(self):
        dr = self.create_dir('root')
        self.assertIsNotNone(dr)
        self.assertEqual(dr.name, 'root')

    def test_add_dir(self):
        root = self.create_dir('root')
        dir_a = self.create_dir('dir_a')

        root.add_sub_dir(dir_a)
        self.assertIsNotNone(root.sub_dirs.get(name=dir_a.name))

        # test avoid duplicate
        root.add_sub_dir(dir_a)
        self.assertEqual(len(root.sub_dirs.filter(name=dir_a.name)), 1)

        # test add multiple sub dirs
        dir_b = self.create_dir('dir_b')
        root.add_sub_dir(dir_b)
        self.assertEqual(len(root.sub_dirs.all()), 2)

    def test_get_parents(self):
        dir_a = self.create_dir('dir_a')
        dir_b = self.create_dir('dir_b')
        final_dir = self.create_dir('final_dir')

        self.assertEqual(len(final_dir.get_parents()), 0)
        dir_a.add_sub_dir(final_dir)
        self.assertEqual(len(final_dir.get_parents()), 1)
        dir_b.add_sub_dir(final_dir)
        self.assertEqual(len(final_dir.get_parents()), 2)

    def test_remove_sub_dir(self):
        root = self.create_dir('root')
        dir_a = self.create_dir('dir_a')
        root.add_sub_dir(dir_a)
        self.assertEqual(len(root.get_sub_dirs()), 1)
        self.assertEqual(len(Directory.objects.all()), 2)

        root.remove_sub_dir(dir_a)
        self.assertEqual(len(root.get_sub_dirs()), 0)
        self.assertEqual(len(Directory.objects.all()), 1)

    def test_remove_sub_dir_two_parents(self):
        p_a = self.create_dir('parent_a')
        p_b = self.create_dir('parent_b')
        sub_dir = self.create_dir('dir_a')
        p_a.add_sub_dir(sub_dir)
        p_b.add_sub_dir(sub_dir)
        self.assertEqual(len(sub_dir.get_parents()), 2)
        self.assertEqual(len(Directory.objects.all()), 3)

        p_a.remove_sub_dir(sub_dir)
        # sub_dir should not be removed since it still has a parent !
        self.assertEqual(len(Directory.objects.all()), 3)

        p_b.remove_sub_dir(sub_dir)
        # sub_dir should be removed since it is isolated !
        self.assertEqual(len(Directory.objects.all()), 2)

    def test_remove_sub_dir_recursively(self):
        """
        create the dir graph:
            root
         /   |    \
       a     b     c
        \   |      |
        ab_a      /
       /   \    /
    ab_a_a  ab_a_b
        """
        root = self.create_dir('root')
        a = self.create_dir('a')
        b = self.create_dir('b')
        c = self.create_dir('c')
        ab_a = self.create_dir('ab_a')
        ab_a_a = self.create_dir('ab_a')
        ab_a_b = self.create_dir('ab_a_b')

        root.add_sub_dir(a).add_sub_dir(b).add_sub_dir(c)
        a.add_sub_dir(ab_a)
        b.add_sub_dir(ab_a)
        ab_a.add_sub_dir(ab_a_a).add_sub_dir(ab_a_b)
        c.add_sub_dir(ab_a_b)
        self.assertEqual(len(Directory.objects.all()), 7)
        self.assertEqual(len(SubDirRelation.objects.all()), 8)

        a.remove_sub_dir(ab_a)
        # object 'ab_a' not removed because there is a link,
        # but the there is one link less
        self.assertEqual(len(Directory.objects.all()), 7)
        self.assertEqual(len(SubDirRelation.objects.all()), 7)

        # 'ab_a' and 'ab_a_a' are deleted,
        # 'ab_a_b' is not because it's linked to c
        b.remove_sub_dir(ab_a)
        self.assertEqual(len(Directory.objects.all()), 5)
        self.assertEqual(len(SubDirRelation.objects.all()), 4)
        try:
            Directory.objects.get(name=ab_a.name)
            self.fail("'%s' should not exist!" % ab_a.name)
        except ObjectDoesNotExist:
            pass
        try:
            Directory.objects.get(name=ab_a_a.name)
            self.fail("'%s' should not exist!" % ab_a_a.name)
        except ObjectDoesNotExist:
            pass

        self.assertIsNotNone(Directory.objects.get(name=ab_a_b.name))
        c.remove_sub_dir(ab_a_b)
        try:
            Directory.objects.get(name=ab_a_b.name)
            self.fail("'%s' should not exist!" % ab_a_b.name)
        except ObjectDoesNotExist:
            pass