from flask import Blueprint

health = Blueprint('health', __name__)


@health.route('/health')
def index():
    return 'OK'
