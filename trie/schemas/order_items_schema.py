from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship

from trie.schemas.base import BaseSchema


class OrderItemsSchema(BaseSchema):

    id = fields.UUID(dump_only=True)
    quantity = fields.Int(required=True)

    store = Relationship(
        related_view='stores.storesapi',
        related_view_kwargs={'id': '<id>'},
        include_data=True,
        type_='stores',
        many=False,
        required=True,
    )

    member = Relationship(
        related_view='members.membersapi',
        related_view_kwargs={'id': '<id>'},
        include_data=True,
        type_='members',
        many=False,
        required=True,
    )

    order = Relationship(
        related_view='orders.ordersapi',
        related_view_kwargs={'id': '<id>'},
        include_data=True,
        type_='orders',
        many=False,
        required=True,
    )

    product = Relationship(
        related_view='products.productsapi',
        related_view_kwargs={'id': '<id>'},
        include_data=True,
        type_='products',
        many=False,
        required=True,
    )

    class Meta:
        type_ = 'order_items'
        strict = True
