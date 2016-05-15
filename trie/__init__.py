from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from trie.utils.configuration import config
from trie.views.health import health
from trie.views.home import home

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{}:{}@{}:{}/{}'.format(
    config.get('database.user'),
    config.get('database.password'),
    config.get('database.host'),
    config.get('database.port'),
    config.get('database.name'),
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set up the database
db = SQLAlchemy(app)

app.register_blueprint(health)
app.register_blueprint(home)
