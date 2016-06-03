from flask import Blueprint
from flask_restful import Api

from trie.models.order import Order
from trie.schemas.orders_schema import OrdersSchema
from trie.views.base import BaseAPI
from trie.views.base import BaseListAPI


orders_blueprint = Blueprint('orders', __name__, url_prefix='/orders')
api = Api(orders_blueprint)


class OrdersListAPI(BaseListAPI):

    model = Order
    schema_model = OrdersSchema


class OrdersAPI(BaseAPI):

    model = Order
    schema_model = OrdersSchema

api.add_resource(OrdersListAPI, '/')
api.add_resource(OrdersAPI, '/<id>')
