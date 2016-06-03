from flask import Blueprint
from flask_restful import Api

from trie.models.order_item import OrderItem
from trie.schemas.order_items_schema import OrderItemsSchema
from trie.views.base import BaseAPI
from trie.views.base import BaseListAPI


order_items_blueprint = Blueprint('order_items', __name__, url_prefix='/order_items')
api = Api(order_items_blueprint)


class OrderItemsListAPI(BaseListAPI):

    model = OrderItem
    schema_model = OrderItemsSchema


class OrderItemsAPI(BaseAPI):

    model = OrderItem
    schema_model = OrderItemsSchema

api.add_resource(OrderItemsListAPI, '/')
api.add_resource(OrderItemsAPI, '/<id>')
