from marshmallow_jsonapi import fields

from trie.schemas.base import BaseSchema
from trie.schemas.base import not_empty


class ProductsSchema(BaseSchema):

    id = fields.UUID(dump_only=True)
    description = fields.String(required=True, validate=not_empty)
    image = fields.String(required=True, validate=not_empty)
    price = fields.Decimal(required=True, validate=not_empty, as_string=True, places=2)
    title = fields.String(required=True, validate=not_empty)

    class Meta:
        type_ = 'products'
        strict = True
