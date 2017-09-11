import random
from fabric.contrib.files import append, exists, sed
from fabric.api import local, env, run

REPO_URL = 'https://github.com/sdotzhang/superlist.git'


def deploy():
    site_folder = '/home/%s/sites/%s' % (env.user, env.host)
    source_folder = "%s/source" % site_folder
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)


def _create_directory_structure_if_necessary(site_folder):
    for subfoler in ('database', 'static', 'source', 'virtualenv'):
        run('mkdir -p %s/%s' % (site_folder, subfoler))


def _get_latest_source(source_folder):
    if exists("%s/.git" % (source_folder)):
        run('cd %s && git pull --rebase' % source_folder)
    else:
        run('git clone %s %s' % (REPO_URL, source_folder))
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run('cd %s && git reset --hard %s' % (source_folder, current_commit))


def _update_settings(source_folder, site_name):
    setting_path = '%s/superlists/settings.py' % source_folder
    sed(setting_path, 'DEBUG = True', 'DEBUG = False')
    sed(setting_path, 'ALLOWED_HOSTS =.+$', 'ALLOWED_HOSTS = ["%s"]' % site_name)
    secret_key_file = "%s/superlists/secret_key.py" % source_folder
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = %s" % key)
    append(setting_path, '\nfrom .secret_key import SECRET_KEY')


def _update_virtualenv(source_folder):
    virtualenv_folder = '%s/../virtualenv' % source_folder
    if not exists("%s/bin/pip" % virtualenv_folder):
        run('virtualenv --python=python3 %s' % (virtualenv_folder))
    run('%s/bin/pip install -r %s/requirements.txt' % (virtualenv_folder, source_folder))


def _update_static_files(source_folder):
    run('cd %s && ../virtualenv/bin/python3 manage.py collectstatic --noinput' % source_folder)


def _update_database(source_folder):
    run('cd %s && ../virtualenv/bin/python3 manage.py migrate --noinput' % source_folder)
