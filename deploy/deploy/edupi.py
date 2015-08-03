import os
from fabric.contrib.files import exists
from fabric.api import run, put

from .helper import send_file, get_config_file
from .settings import RASP_USER_NAME, DEFAULT_PASSWORD

REPO_URL = 'https://github.com/yuancheng2013/edupi.git'

SOURCE_DIR_NAME = 'edupi'

EDUPI_SITE_NAME = 'edupi.fondationorange.org'


class EdupiDeployManager():
    def __init__(self):
        self.site_folder = '/home/%s/sites/%s' % (RASP_USER_NAME, EDUPI_SITE_NAME)
        self.source_folder = os.path.join(self.site_folder, SOURCE_DIR_NAME)
        self.nginx_config = '/etc/nginx/sites-enabled/%s' % EDUPI_SITE_NAME
        self.upstart_config = '/etc/init/gunicorn-%s.conf' % EDUPI_SITE_NAME

    def deploy(self, commit):
        # Nginx conf
        send_file(self.nginx_config)
        # Nginx logrotate config
        send_file('/etc/logrotate.d/nginx', mod='644')
        # Upstart
        send_file(self.upstart_config)

        self._create_directory_structure_if_necessary(self.site_folder)
        self._get_source(self.source_folder, commit)
        self._update_virtualenv(self.source_folder)
        self._update_static_files(self.source_folder)
        self._update_database(self.source_folder)

        # reboot the application
        run('sudo restart gunicorn-%s' % EDUPI_SITE_NAME)

    @staticmethod
    def _create_directory_structure_if_necessary(site_folder):
        for subfolder in ('database', 'static', 'media', 'stats', 'virtualenv', SOURCE_DIR_NAME):
            run('mkdir -p %s/%s' % (site_folder, subfolder))
        # nginx log file
        run('sudo mkdir -p /var/log/nginx/edupi/')

    @staticmethod
    def _get_source(source_folder, commit):
        if exists(source_folder + '/.git'):
            run('cd %s && git fetch' % (source_folder,))
        else:
            run('git clone %s %s' % (REPO_URL, source_folder))

        run('cd %s && git reset --hard %s' % (source_folder, commit))

    @staticmethod
    def _update_virtualenv(source_folder):
        virtualenv_folder = source_folder + '/../virtualenv'
        if not exists(virtualenv_folder + '/bin/pip3'):
            run('virtualenv --python=python3.4 %s' % (virtualenv_folder,))
        run('%s/bin/pip install -r %s/requirements.txt' % (
            virtualenv_folder, source_folder
        ))

    @staticmethod
    def _update_static_files(source_folder):
        # install Front-End packages
        # assume that node.js, npm, bower is installed
        run('cd %s && ../virtualenv/bin/python3 manage.py bower install' % source_folder)
        run('cd %s && ../virtualenv/bin/python3 manage.py collectstatic --noinput' % source_folder)

    @staticmethod
    def _update_database(source_folder):
        run('cd %s && ../virtualenv/bin/python3 manage.py migrate --noinput' % (
            source_folder,
        ))
        # ensure that there is a default super user.
        run("""
cd %s &&
echo "
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
try:
    User.objects.create_superuser('%s', '', '%s')
except IntegrityError as e:  # user exists
    print(e)
" |
../virtualenv/bin/python3 manage.py shell
            """
            % (source_folder, RASP_USER_NAME, DEFAULT_PASSWORD))
