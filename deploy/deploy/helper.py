import os
from fabric.contrib.files import exists
from fabric.api import run, put

CONFIG_TEMPLATES_FOLDER = 'sysconf'


def send_file(abs_path, use_sudo=True, mod='755'):
    """
    send local file to remote host
    """
    put(get_config_file(abs_path), abs_path, use_sudo=use_sudo)
    run('sudo chmod %s %s' % (mod, abs_path))
    if use_sudo:
        run('sudo chown root:root %s' % abs_path)


def get_config_file(path):
    if path[0] != '/':
        print 'please input the absolute path'
        exit(-1)

    f = os.path.join(os.getcwd(), CONFIG_TEMPLATES_FOLDER, path[1:])
    if not os.path.exists(f):
        print "'%s' does not exist" % f
        exit(-1)
    return f
