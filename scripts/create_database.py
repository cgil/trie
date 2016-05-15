"""Create the production database."""

import os

from fabric.api import local
from fabric.context_managers import settings

os.environ['CONFIG_ENV'] = './config/production.yaml'

from trie.utils.configuration import config


with settings(warn_only=True):
    # Create a new role
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
