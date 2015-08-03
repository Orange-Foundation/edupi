"""
reference: https://github.com/hjwp/book-example/blob/master/deploy_tools/fabfile.py
"""

from fabric.contrib.files import exists
from fabric.api import run

from deploy.edupi import EdupiDeployManager
from deploy.settings import RASP_USER_NAME
from deploy.helper import send_file


__all__ = [
    'config_hotspot',
    'install_deps',
    'deploy_edupi',
    'uninstall_edupi',
    'deploy_index_page'
]


PORTAL_SITE_NAME = 'fondationorange.org'


def install_deps():
    run('sudo apt-get update')
    run('sudo apt-get install -y nginx')
    run('sudo apt-get install -y python3-pip')
    run('sudo apt-get install -y libmagickwand-dev')
    run('sudo apt-get install upstart')  # this will prompt and wait for confirm

    run('sudo pip-3.2 install virtualenv')

    # install nodejs, bower
    nodejs_path = '/tmp/node_latest_armhf.deb'
    if not exists(nodejs_path):
        run('wget http://node-arm.herokuapp.com/node_latest_armhf.deb --directory-prefix=/tmp/')

    run('sudo dpkg -i %s' % nodejs_path)
    run('curl -L https://www.npmjs.com/install.sh | sudo sh')
    run('sudo npm install -g bower')


def config_hotspot():
    run('sudo apt-get update')
    run('sudo apt-get install -y hostapd dnsmasq')
    config_files = [
        '/etc/network/interfaces',
        '/etc/dnsmasq.conf',
        '/etc/resolvconf.conf',
        '/etc/hostapd/hostapd.conf.orig',
        '/etc/rc.local',
        ]

    list(map(send_file, config_files))
    run('sudo reboot')


def deploy_edupi(commit='origin/release'):
    manager = EdupiDeployManager()
    manager.deploy(commit)


def uninstall_edupi(purge_data=False):
    manager = EdupiDeployManager()
    manager.uninstall(purge_data)


def deploy_index_page():
    site_folder = '/home/%s/sites/www' % RASP_USER_NAME
    repo_url = 'https://github.com/yuancheng2013/raspberry-index-page.git'
    # Nginx conf
    send_file('/etc/nginx/sites-enabled/%s' % PORTAL_SITE_NAME)

    # create site folder
    run('mkdir -p %s' % site_folder)

    # Get source
    if exists(site_folder + '/.git'):
        run('cd %s && git fetch' % site_folder)
    else:
        run('cd %s && rm -fr *' % site_folder)
        run('git clone %s %s' % (repo_url, site_folder))

    # force to use latest source on the master branch
    run('cd %s && git reset --hard %s' % (site_folder, 'origin/master'))
