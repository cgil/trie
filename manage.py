from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from trie import create_app
from trie.database import db

app = create_app()

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.shell
def make_shell_context():
    return dict(app=app, db=db)

if __name__ == '__main__':
    manager.run()
