from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from trie import app
from trie import db

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
