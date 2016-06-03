from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship

from trie.schemas.base import BaseSchema
from trie.schemas.base import not_empty


class OrdersSchema(BaseSchema):

    id = fields.UUID(dump_only=True)

    financial_status = fields.String(required=True)
    fulfillment_status = fields.String()
    total_price = fields.Decimal(required=True, validate=not_empty, as_string=True, places=2)
    shipping_address_city = fields.String()
    shipping_address_country = fields.String()
    shipping_address_country_code = fields.String()
    shipping_address_1 = fields.String()
    shipping_address_zip = fields.String()
    shipping_name = fields.String()

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

    class Meta:
        type_ = 'orders'
        strict = True
