import os
import sys

from fabric.api import local
from fabric.api import task
from fabric.colors import green
from fabric.colors import red
from fabric.context_managers import settings

DEFAULT_ENV = 'development'


@task
def clean():
    """Remove all .pyc files."""
    print green('Clean up .pyc files')
    local("find . -name '*.py[co]' -exec rm -f '{}' ';'")


@task
def shell(env=DEFAULT_ENV):
    """Run the shell in the environment."""
    os.environ['CONFIG_ENV'] = './config/%s.yaml' % env
    local('python manage.py shell')


@task
def test(args='', env='test'):
    """Run tests."""
    os.environ['CONFIG_ENV'] = './config/%s.yaml' % env
    clean()
    print green('Running all tests')
    cmd = ('nosetests -d --verbosity 3 --with-id --nocapture %s' % args)

    with settings(warn_only=True, quiet=True):
        success = local(cmd).succeeded

    lint()

    if success:
        print(green('Tests finished running with success.'))
    else:
        print(red('Test finished running with errors.'))
        sys.exit(1)


@task
def lint():
    """Check for lints"""
    print green('Checking for lints')
    return local("flake8 `find . -name '*.py' -not -path '*env/*'` "
                 "--ignore=E711,E712 --max-line-length=100").succeeded


@task
def db(env=DEFAULT_ENV):
    """Connect to the database."""
    os.environ['CONFIG_ENV'] = './config/%s.yaml' % env
    from trie.utils.configuration import config
    local(
        'psql -h {} -p {} -U {} {}'.format(
            config.get('database.host'),
            config.get('database.port'),
            config.get('database.user'),
            config.get('database.name'),
        ),
    )


@task
def bootstrap_database(env=DEFAULT_ENV):
    """Bootstrap the database."""
    os.environ['CONFIG_ENV'] = './config/%s.yaml' % env
    from trie.utils.configuration import config
    with settings(warn_only=True):
        # Create a new role
        local(
            'psql -h {} -p {} -c "CREATE ROLE {} WITH ENCRYPTED PASSWORD \'{}\' '
            'SUPERUSER CREATEDB CREATEROLE LOGIN;"'.format(
                config.get('database.host'),
                config.get('database.port'),
                config.get('database.user'),
                config.get('database.password'),
            )
        )
        # Drop the existing database if it exists
        local(
            'dropdb -U {} -h {} -p {} -w {} --if-exists'.format(
                config.get('database.user'),
                config.get('database.host'),
                config.get('database.port'),
                config.get('database.name'),
            )
        )
        # Create the database
        res = local(
            'createdb -h {} -p {} -U {} -w -E UTF8 -O {} {}'.format(
                config.get('database.host'),
                config.get('database.port'),
                config.get('database.user'),
                config.get('database.user'),
                config.get('database.name'),
            )
        )
        if not res.succeeded:
            print red('Failed to bootstrap the database.')
            return

        # Migrate tables
        res = local('python manage.py db upgrade head')
        if not res.succeeded:
            print red('Failed to migrate tables.')
            return

        print green('Successfully migrated the database.')


@task
def bootstrap(env=DEFAULT_ENV):
    """Bootstrap the environment."""
    os.environ['CONFIG_ENV'] = './config/%s.yaml' % env
    local('mkdir -p logs')
    print green('\nInstalling requirements')
    local('pip install -r requirements-test.txt')
    local('pip install -r requirements-development.txt')
    local('pip install -r requirements.txt')
    local('python setup.py develop')


@task
def serve(env=DEFAULT_ENV):
    """Start the server."""
    os.environ['CONFIG_ENV'] = './config/%s.yaml' % env
    local('python app.py')
