from django.apps import AppConfig

import logging

logger = logging.getLogger(__name__)


class CntappConfig(AppConfig):
    name = 'cntapp'

    def ready(self):
        # app init code here
        # ensure that the lock file is deleted
        from cntapp.views.stats import StatsLockManager
        if StatsLockManager.is_locked():
            logger.warn('The stats lock was not released. Unlock now!')
            StatsLockManager.unlock()
