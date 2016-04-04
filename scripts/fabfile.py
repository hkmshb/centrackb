from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import os, random


REPO_URL = 'https://kedco_abdulhakeem@bitbucket.org/kedco_abdulhakeem/centrackb.git' 



def deploy(site_name, project_name, repo_url=None):
    site_folder = '/home/%s/webapps/%s' % (env.user, site_name)
    source_folder = site_folder + '/source'
    
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder, repo_url or REPO_URL)
    _update_virtualenv(source_folder)
    _update_uwsgi_file(source_folder, site_name, project_name)
    _update_upstart_file(source_folder, site_name, project_name)
    _update_nginx_conf(source_folder, site_name, project_name)


def _create_directory_structure_if_necessary(site_folder):
    for folder in ('static', 'virtualenv', 'source'):
        run('mkdir -p %s/%s' % (site_folder, folder))


def _get_latest_source(source_folder, repo_url=None):
    if exists(source_folder + '/.git'):
        run('cd %s && git fetch' % (source_folder,))
    else:
        run('git clone %s %s' % (repo_url, source_folder))
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run('cd %s && git reset --hard %s' % (source_folder, current_commit))


def _update_virtualenv(source_folder):
    venv_folder = source_folder + '/../virtualenv'
    if not exists(venv_folder + '/bin/pip'):
        run('virtualenv --python=python3.4 %s' % (venv_folder))
    
    common_file = '%s/requirements/common.txt' % source_folder
    run('%s/bin/pip install -r %s/requirements/common.txt' % (
        venv_folder, source_folder
    ))
    run('%s/bin/pip install -r %s/requirements/linux.txt' % (
        venv_folder, source_folder
    ))


def _update_uwsgi_file(source_folder, site_name, project_name):
    conf_file = source_folder + '/scripts/uwsgi.ini'
    sed(conf_file, '<usr>', env.user)
    sed(conf_file, '<site>', site_name)
    sed(conf_file, '<project>', project_name)


def _update_upstart_file(source_folder, site_name, project_name):
    conf_dir = source_folder + '/scripts/etc/init/'
    conf_file = 'centrackb.conf'
    file_path = conf_dir + conf_file
    sed(file_path, '<usr>', env.user)
    sed(file_path, '<site>', site_name)
    sed(file_path, '<project>', project_name)
    
    cmd = 'cd %s && sudo cp %s /etc/init/'
    if exists('/etc/init/centrackb.conf'):
        cmd = 'sudo rm /etc/init/centrackb.conf && ' + cmd
    run(cmd % (conf_dir, conf_file))


def _update_nginx_conf(source_folder, site_name, project_name):
    conf_dir  = source_folder + '/scripts/etc/nginx/'
    conf_file = 'centrackb.conf'
    file_path = conf_dir + conf_file
    sed(file_path, '<usr>', env.user)
    sed(file_path, '<site>', site_name)
    sed(file_path, '<project>', project_name)
    
    cmd = ('cd %s && sudo cp %s /etc/nginx/sites-available/ &&'
           'cd /etc/nginx/sites-enabled && '
           'sudo ln -s /etc/nginx/sites-available/centrackb.conf centrackb')
    
    if exists('/etc/nginx/sites-enabled/centrackb'):
        cmd = 'sudo rm /etc/nginx/sites-enabled/centrackb && ' + cmd
    run(cmd % (conf_dir, conf_file))

