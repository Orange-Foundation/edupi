"""
credit: https://www.caktusgroup.com/blog/2013/06/26/media-root-and-django-tests/
"""
import os
import shutil
import tempfile

from django.test.runner import DiscoverRunner
from django.conf import settings


class TempMediaMixin(object):
    """ Mixin to create MEDIA_ROOT in temp and tear down when complete.
    """

    def setup_test_environment(self):
        """Create temp directory and update MEDIA_ROOT and default storage."""
        super(TempMediaMixin, self).setup_test_environment()
        settings._original_media_root = settings.MEDIA_ROOT
        settings._original_file_storage = settings.DEFAULT_FILE_STORAGE
        if not os.path.exists(settings._original_media_root):
            os.mkdir(settings._original_media_root)
        self._temp_media = tempfile.mkdtemp(dir=settings._original_media_root)
        settings.MEDIA_ROOT = self._temp_media
        settings.DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

    def teardown_test_environment(self):
        """Delete temp storage."""
        super(TempMediaMixin, self).teardown_test_environment()
        shutil.rmtree(self._temp_media, ignore_errors=True)
        settings.MEDIA_ROOT = settings._original_media_root
        del settings._original_media_root
        settings.DEFAULT_FILE_STORAGE = settings._original_file_storage
        del settings._original_file_storage


class TempStatsMixin(object):
    """ Mixin to create STATS_DIR in temp and tear down when complete.
    """

    def setup_test_environment(self):
        """Create temp directory and update MEDIA_ROOT and default storage."""
        super(TempStatsMixin, self).setup_test_environment()
        settings._original_stats_dir = settings.STATS_DIR
        self._temp_stats = tempfile.mkdtemp(dir='/tmp', prefix='edupi_stats_')
        settings.STATS_DIR = self._temp_stats

    def teardown_test_environment(self):
        """Delete temp storage."""
        super(TempStatsMixin, self).teardown_test_environment()
        shutil.rmtree(self._temp_stats, ignore_errors=True)
        settings.STATS_DIR = settings._original_stats_dir
        del settings._original_stats_dir


class CustomTestSuiteRunner(TempMediaMixin,
                            TempStatsMixin,
                            DiscoverRunner):
    """ Local test suite runner.
    """
