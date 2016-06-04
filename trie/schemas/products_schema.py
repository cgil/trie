from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship

from trie.schemas.base import BaseSchema
from trie.schemas.base import not_empty


class ProductsSchema(BaseSchema):

    id = fields.UUID(dump_only=True)
    description = fields.String(required=True, validate=not_empty)
    image = fields.String(required=True, validate=not_empty)
    price = fields.Decimal(required=True, validate=not_empty, as_string=True, places=2)
    title = fields.String(required=True, validate=not_empty)

    store = Relationship(
        related_view='stores.storesapi',
        related_view_kwargs={'id': '<store_id>'},
        include_data=True,
        type_='stores',
        many=False,
        required=True,
    )

    class Meta:
        type_ = 'products'
        strict = True
