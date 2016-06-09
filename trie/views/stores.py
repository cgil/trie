from flask import Blueprint
from flask import request
from flask_restful import Api

from trie.lib import loggers
from trie.models.store import Store
from trie.schemas.stores_schema import StoresSchema
from trie.views.base import BaseAPI
from trie.views.base import BaseListAPI
from trie.views.base import parse_query_string


stores_blueprint = Blueprint('stores', __name__, url_prefix='/stores')
api = Api(stores_blueprint)

logger = loggers.get_logger(__name__)


class StoresListAPI(BaseListAPI):

    model = Store
    schema_model = StoresSchema


class StoresAPI(BaseAPI):

    model = Store
    schema_model = StoresSchema

    def get(self, id):
        """Get a single record."""
        query_params = parse_query_string(request.query_string)
        logger.info({
            'msg': 'Getting a record.',
            'view': self.__class__.__name__,
            'method': 'get',
            'schema_model': self.schema_model.__name__,
            'model': self.model.__name__,
            'record_id': id,
            'query_params': query_params,
        })
        record = self.model.get_or_404(id)
        result = self.schema.dump(record).data

        # Filter products in the result.
        # TODO: Fix this - should not iterate on results, move to base, make generic.
        filter_products = query_params.get('filter', {}).get('product', [])
        filter_products = [product.replace('-', '') for product in filter_products]
        if filter_products:
            products = result['data']['attributes']['products']['data']
            for product in list(products):
                if product['id'].replace('-', '') not in filter_products:
                    products.remove(product)
        return result


api.add_resource(StoresListAPI, '/')
api.add_resource(StoresAPI, '/<id>')
