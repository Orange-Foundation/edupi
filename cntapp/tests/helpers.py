from django.core.files.uploadedfile import SimpleUploadedFile

from cntapp.models import Directory, Document
import factory


def create_dir(name):
    d = Directory(name=name)
    d.save()
    return d


def init_test_dirs():
    """
    create the dir graph:
   a     b     c
    \   |      |
    ab_a      /
   /   \    /
ab_a_a  ab_a_b
    """
    a = create_dir('a')
    b = create_dir('b')
    c = create_dir('c')
    ab_a = create_dir('ab_a')
    ab_a_a = create_dir('ab_a_a')
    ab_a_b = create_dir('ab_a_b')

    a.add_sub_dir(ab_a)
    b.add_sub_dir(ab_a)
    ab_a.add_sub_dir(ab_a_a).add_sub_dir(ab_a_b)
    c.add_sub_dir(ab_a_b)


DIRECTORY_BASE_NAME = '__test_directory__'
DOCUMENT_BASE_NAME = '__test_document__'
DESCRIPTION_BASE_TEXT = '__description__'


class DocumentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Document


class PdfDocumentFactory(DocumentFactory):
    name = factory.Sequence(lambda n: '%s%d.pdf' % (DOCUMENT_BASE_NAME, n))
    description = factory.Sequence(lambda n: '%s%d' % (DESCRIPTION_BASE_TEXT, n))
    type = Document.TYPE_PDF
    file = factory.LazyAttribute(lambda a: SimpleUploadedFile(a.name, a.description.encode('utf-8')))


class DirectoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Directory

    name = factory.Sequence(lambda n: '%s%d' % (DIRECTORY_BASE_NAME, n))
