from flask import Blueprint
from flask import render_template

home = Blueprint('home', __name__, template_folder='trie/templates')

@home.route('/')
def index():
    return render_template('index.html')
