from flask import Blueprint
from flask_restful import Api

from trie.models.product import Product
from trie.schemas.products_schema import ProductsSchema
from trie.views.base import BaseAPI
from trie.views.base import BaseListAPI


products_blueprint = Blueprint('products', __name__, url_prefix='/products')
api = Api(products_blueprint)


class ProductsListAPI(BaseListAPI):

    model = Product
    schema_model = ProductsSchema


class ProductsAPI(BaseAPI):

    model = Product
    schema_model = ProductsSchema

api.add_resource(ProductsListAPI, '/')
api.add_resource(ProductsAPI, '/<id>')
