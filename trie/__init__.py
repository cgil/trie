import os

from flask import Flask

from trie.database import db
from trie.utils.configuration import config
from trie.views.health import health
from trie.views.home import home


def create_app():
    """Create and initialize the application."""
    database_url = os.environ.get('DATABASE_URL') or 'postgres://{}:{}@{}:{}/{}'.format(
        config.get('database.user'),
        config.get('database.password'),
        config.get('database.host'),
        config.get('database.port'),
        config.get('database.name'),
    )
    app = Flask(__name__)
    app.secret_key = config.get('secret_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Set up the database
    db.init_app(app)

    # register blueprints
    app.register_blueprint(health)
    app.register_blueprint(home)
    return app
