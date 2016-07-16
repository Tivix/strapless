from __future__ import absolute_import

import os
from datetime import datetime

from django.conf import settings

from fabric.api import local, run, env, get
from fabric.decorators import runs_once
from fabric.context_managers import shell_env


DEFAULT_DB_SETTINGS = settings.DATABASES['default']


def staging():
    """Sets up the staging environment for fab remote commands"""
    from strapless_web.settings import staging
    env.ENV = 'staging'
    env.user = 'ubuntu'
    env.hosts = staging.SSH_HOSTS[0]
    env.source = staging


def freshdb():
    local('sudo -u postgres dropdb %s' % settings.DATABASES['default']['NAME'])
    env.warn_only = False
    local('sudo -u postgres createdb %s' %
          settings.DATABASES['default']['NAME'])


def dumpdb():
    env.keepalive = 1800
    env.database = env.source.DATABASES['default']
    DUMP_FILENAME = 'dump-%s.sql' % datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

    env.warn_only = True

    postgres_command = 'pg_dump -w -Fc -U {user} -h {host} -p {port} {dbname} > /tmp/{file}'.format(**{
        'file': DUMP_FILENAME,
        'dbname': env.database['NAME'],
        'host': env.database['HOST'],
        'port': env.database.get('PORT', 5432),
        'user': env.database['USER'],
    })

    with shell_env(PGPASSWORD=env.database['PASSWORD']):
        run(postgres_command)
    get('/tmp/%s' % DUMP_FILENAME, os.path.basename(DUMP_FILENAME))
    return DUMP_FILENAME


def syncdb():
    """Gets a copy of the remote db and puts it into dev environment"""
    env.keepalive = 1800
    env.database = settings.DATABASES['default']
    DUMP_FILENAME = dumpdb()
    freshdb()
    local('sudo -u postgres pg_restore --verbose --no-acl --no-owner -d %s < %s' %
          (env.database['NAME'], DUMP_FILENAME))
    local('rm %s' % DUMP_FILENAME)
    run('rm /tmp/%s' % DUMP_FILENAME)


@runs_once
def sync_uploads():
    """Reset local media from remote host"""
    local("rsync -rva ubuntu@%s:webapps/%s/uploads/ %s" % (
        env.host_string, settings.PROJECT_NAME, settings.MEDIA_ROOT))


def r():
    """
    Shortcut to do quick runserver
    """

    local('python manage.py runserver 0.0.0.0:8000')


def sp():
    """
    Shortcut to do shell_plus
    """

    local('python manage.py shell_plus')

runserver = r  # alias
