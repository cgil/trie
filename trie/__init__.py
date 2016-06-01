import os

from flask import Flask
from flask import Response
from flask import current_app
from flask import json
from flask import request
from flask.ext.cors import CORS

from trie.database import db
from trie.login_manager import login_manager
from trie.utils.configuration import config
from trie.views.health import health
from trie.views.home import home
from trie.views.products import products_blueprint
from trie.views.stores import stores_blueprint


class ResponseJSON(Response):
    """Extend flask.Response with support for list/dict conversion to JSON."""
    def __init__(self, content=None, *args, **kargs):
        if isinstance(content, (list, dict)):
            kargs['mimetype'] = 'application/json'
            content = to_json(content)

        super(Response, self).__init__(content, *args, **kargs)

    @classmethod
    def force_type(cls, response, environ=None):
        """Override with support for list/dict."""
        if isinstance(response, (list, dict)):
            return cls(response)
        else:
            return super(Response, cls).force_type(response, environ)


def to_json(content):
    """Converts content to json while respecting config options."""
    indent = None
    separators = (',', ':')

    if (current_app.config['JSONIFY_PRETTYPRINT_REGULAR']
            and not request.is_xhr):
        indent = 2
        separators = (', ', ': ')

    return (json.dumps(content, indent=indent, separators=separators), '\n')


class FlaskJSON(Flask):
    """Extension of standard Flask app with custom response class."""
    response_class = ResponseJSON


def create_app():
    """Create and initialize the application."""
    database_url = os.environ.get('DATABASE_URL') or 'postgres://{}:{}@{}:{}/{}'.format(
        config.get('database.user'),
        config.get('database.password'),
        config.get('database.host'),
        config.get('database.port'),
        config.get('database.name'),
    )
    app = FlaskJSON(__name__)
    app.secret_key = config.get('secret_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Set up CORS
    # TODO: Revisit in the future. Set up more granular access per view.
    CORS(app)

    # Set up the database
    db.init_app(app)

    # Set up the user session
    login_manager.init_app(app)

    # register blueprints
    app.register_blueprint(health)
    app.register_blueprint(home)
    app.register_blueprint(products_blueprint)
    app.register_blueprint(stores_blueprint)
    return app
