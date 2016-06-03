from marshmallow import validate
from marshmallow_jsonapi import fields

from trie.schemas.base import BaseSchema
from trie.schemas.orders_schema import OrdersSchema


class MembersSchema(BaseSchema):

    id = fields.UUID(dump_only=True)

    email = fields.String(required=True)
    password = fields.String(load_only=True, validate=validate.Length(4))
    stripe_customer_id = fields.String(load_only=True)

    orders = fields.Nested(
        OrdersSchema,
        many=True,
    )

    class Meta:
        type_ = 'members'
        strict = True
        exclude = ('password', 'stripe_customer_id')
