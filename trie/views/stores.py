from flask import Blueprint
from flask_restful import Api
from flask_restful import Resource

from trie.models.store import Store
from trie.schemas.stores_schema import StoresSchema
from trie.views.base import BaseAPI
from trie.views.base import BaseListAPI


stores_blueprint = Blueprint('stores', __name__)
api = Api(stores_blueprint)


class StoresListAPI(BaseListAPI):

    model = Store
    schema_model = StoresSchema


class StoresAPI(BaseAPI):

    model = Store
    schema_model = StoresSchema


class StoresMiscAPI(Resource):

    model = Store
    schema_model = StoresSchema

    def get(self, id):
        """Get a single store record."""
        record = self.model.get_or_404(id)
        result = self.schema.dump(record).data
        return result


api.add_resource(StoresListAPI, '/stores/')
api.add_resource(StoresAPI, '/stores/<id>', '/<id>')
api.add_resource(StoresMiscAPI, '/<id>')
