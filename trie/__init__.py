from flask import Flask

from trie.views.health import health
from trie.views.home import home

app = Flask(__name__)
app.register_blueprint(health)
app.register_blueprint(home)
