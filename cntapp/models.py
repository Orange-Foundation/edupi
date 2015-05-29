import datetime

from django.dispatch.dispatcher import receiver

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.db import models
from django.db.models.signals import post_save, post_delete, m2m_changed
from django.core.cache import cache

import logging

logger = logging.getLogger(__name__)


class Document(models.Model):
    TYPE_VIDEO = 'v'
    TYPE_PDF = 'p'
    TYPE_IMAGE = 'i'
    TYPE_AUDIO = 'a'
    TYPE_GOOGLE_APK = 'g'  # for google ;)
    TYPE_OTHERS = 'o'
    TYPES = (
        (TYPE_VIDEO, 'video'),
        (TYPE_AUDIO, 'sound'),
        (TYPE_PDF, 'pdf'),
        (TYPE_GOOGLE_APK, 'google_apk'),
        (TYPE_IMAGE, 'image'),
        (TYPE_OTHERS, 'others'),
    )

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=2, choices=TYPES, blank=True)
    description = models.CharField(max_length=250, blank=True)
    file = models.FileField()
    thumbnail = ProcessedImageField(upload_to='thumbnails', blank=True, null=True,
                                    processors=[ResizeToFill(400, 400)],
                                    format='PNG',
                                    options={'quality': 99})

    def __str__(self):
        return self.name


# Receive the post signal and delete the file associated with the document instance.
@receiver(post_delete, sender=Document)
def document_delete(sender, instance, **kwargs):
    instance.file.delete(False)
    instance.thumbnail.delete(False)


class Directory(models.Model):
    MAX_NAME_LEN = 255
    name = models.CharField(max_length=MAX_NAME_LEN)
    documents = models.ManyToManyField(Document, blank=True)
    sub_dirs = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        through='SubDirRelation',
        through_fields=('parent', 'child'))

    def get_sub_dirs(self):
        return self.sub_dirs.all()

    def get_sub_dir_by_name(self, name):
        dirs = self.get_sub_dirs()
        return dirs.get(name=name)

    def get_parents(self):
        return self.directory_set.all()

    def add_sub_dir(self, sub_dir):
        if len(SubDirRelation.objects.filter(parent=self, child=sub_dir)) > 0:
            # TODO: warning
            return self
        SubDirRelation.objects.create(parent=self, child=sub_dir)
        return self

    def remove_sub_dir(self, sub_dir):
        l = SubDirRelation.objects.get(parent=self, child=sub_dir)
        if l is None:
            # TODO: warning
            return
        l.delete()
        if len(sub_dir.get_parents()) == 0:
            for d in sub_dir.get_sub_dirs():
                sub_dir.remove_sub_dir(d)
            Directory.objects.get(pk=sub_dir.pk).delete()

    def unlink_sub_dir(self, sub_dir):
        try:
            l = SubDirRelation.objects.get(parent=self, child=sub_dir)
            l.delete()
            return True
        except models.ObjectDoesNotExist as e:
            logger.warn('No SubDirRelation found between parent_id=%d and child_id=%d: %s' % (
                self.id, sub_dir.id, e
            ))
            return False

    def __str__(self):
        return self.name


class SubDirRelation(models.Model):
    parent = models.ForeignKey(Directory, related_name='parent')
    child = models.ForeignKey(Directory, related_name='child')


def change_api_updated_at(sender=None, instance=None, *args, **kwargs):
    cache.set('api_updated_at_timestamp', datetime.datetime.utcnow())

for model in [Document, Directory]:
    post_save.connect(receiver=change_api_updated_at, sender=model)
    post_delete.connect(receiver=change_api_updated_at, sender=model)

for through in [Directory.sub_dirs.through, Directory.documents.through]:
    m2m_changed.connect(receiver=change_api_updated_at, sender=through)
