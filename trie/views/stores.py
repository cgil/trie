from flask import Blueprint
from flask_restful import Api

from trie.models.store import Store
from trie.schemas.stores_schema import StoresSchema
from trie.views.base import BaseAPI
from trie.views.base import BaseListAPI


stores_blueprint = Blueprint('stores', __name__, url_prefix='/stores')
api = Api(stores_blueprint)


class StoresListAPI(BaseListAPI):

    model = Store
    schema_model = StoresSchema


class StoresAPI(BaseAPI):

    model = Store
    schema_model = StoresSchema

api.add_resource(StoresListAPI, '/')
api.add_resource(StoresAPI, '/<id>')
