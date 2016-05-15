from fabric.api import local


local('alembic upgrade head')
