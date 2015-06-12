from django.test import TestCase

from django.db.models import ObjectDoesNotExist

from cntapp.models import Directory, Document, SubDirRelation
from .helpers import DocumentFactory, PdfDocumentFactory, DirectoryFactory, init_test_dirs
from .helpers import DOCUMENT_BASE_NAME, DIRECTORY_BASE_NAME


class DocumentTest(TestCase):
    def setUp(self):
        super(DocumentTest, self).setUp()
        DocumentFactory.reset_sequence(force=True)

    def test_create_and_delete_document(self):
        d = PdfDocumentFactory()
        self.assertEqual(DOCUMENT_BASE_NAME + '0.pdf', d.name)
        self.assertEqual(1, len(Document.objects.all()))

        d = Document.objects.get(id=1)
        self.assertEqual(DOCUMENT_BASE_NAME + '0.pdf', d.name)
        d.delete()
        self.assertEqual(0, len(Document.objects.all()))

    def test_add_and_delete_document_in_dir(self):
        """
        d1      d0
        |     __|_________
        \    |     |     |
         -->f_1   f_2   f_3
        """
        d0 = DirectoryFactory()
        d1 = DirectoryFactory()
        f_1 = PdfDocumentFactory()
        f_2 = PdfDocumentFactory()
        f_3 = PdfDocumentFactory()

        d0.documents.add(f_1)
        d0.documents.add(f_2)
        d0.documents.add(f_3)
        d1.documents.add(f_1)

        self.assertEqual(3, len(d0.documents.all()))
        self.assertEqual(1, len(d1.documents.all()))
        self.assertEquals(3, len(Document.objects.all()))
        self.assertEquals(2, len(f_1.directory_set.all()))

        d0.documents.remove(f_1)
        self.assertEqual(2, len(d0.documents.all()))
        self.assertEqual(1, len(d1.documents.all()))
        self.assertEquals(1, len(f_1.directory_set.all()))

        d1.documents.remove(f_1)
        self.assertEqual(0, len(d1.documents.all()))
        self.assertEquals(0, len(f_1.directory_set.all()))
        self.assertEquals(3, len(Document.objects.all()))

    def test_get_parents(self):
        d0 = DirectoryFactory()
        d1 = DirectoryFactory()
        f_1 = PdfDocumentFactory()
        d0.documents.add(f_1)
        d1.documents.add(f_1)
        self.assertEqual(2, f_1.directory_set.count())

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

    def test_remove_not_sub_dir(self):
        root = self.create_dir('root')
        dir_a = self.create_dir('dir_a')
        with self.assertRaises(SubDirRelation.DoesNotExist):
            root.remove_sub_dir(dir_a)

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

    def test_unlink_directory(self):
        init_test_dirs()
        ab_a = Directory.objects.get(name='ab_a')
        ab_a_a = Directory.objects.get(name='ab_a_a')
        self.assertEqual(6, Directory.objects.count())
        self.assertIn(ab_a_a, ab_a.get_sub_dirs())
        self.assertIn(ab_a, ab_a_a.get_parents())

        # correct unlink
        self.assertTrue(ab_a.unlink_sub_dir(ab_a_a))

        self.assertNotIn(ab_a_a, ab_a.get_sub_dirs())
        self.assertNotIn(ab_a, ab_a_a.get_parents())

        # incorrect unlink
        self.assertFalse(ab_a.unlink_sub_dir(ab_a_a))
        self.assertNotIn(ab_a_a, ab_a.get_sub_dirs())
        self.assertEqual(6, Directory.objects.count())

    def test_get_paths(self):
        init_test_dirs()
        a = Directory.objects.get(name='a')
        b = Directory.objects.get(name='b')
        c = Directory.objects.get(name='c')
        ab_a = Directory.objects.get(name='ab_a')
        ab_a_a = Directory.objects.get(name='ab_a_a')
        ab_a_b = Directory.objects.get(name='ab_a_b')

        path_1 = [a, ab_a, ab_a_a]
        path_2 = [b, ab_a, ab_a_a]

        self.assertEqual([[a]], a.get_paths())
        self.assertEqual([path_1, path_2], ab_a_a.get_paths())
        self.assertEqual(
            [
                [a, ab_a, ab_a_b],
                [b, ab_a, ab_a_b],
                [c, ab_a_b],
            ],
            ab_a_b.get_paths()
        )
