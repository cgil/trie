from marshmallow_jsonapi import fields

from trie.schemas.base import BaseSchema
from trie.schemas.base import not_empty


class StoresSchema(BaseSchema):

    id = fields.UUID(dump_only=True)
    name = fields.String(required=True, validate=not_empty)
    tote_domain = fields.Url(required=True, validate=not_empty)
    domain = fields.Url()
    email = fields.Email()
    address_1 = fields.String()
    city = fields.String()
    zip_code = fields.String()
    country = fields.String()
    country_code = fields.String()
    currency = fields.String()
    phone = fields.String()

    class Meta:
        type_ = 'stores'
        strict = True
