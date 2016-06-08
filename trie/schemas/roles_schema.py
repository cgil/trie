from marshmallow_jsonapi import fields

from trie.schemas.base import BaseSchema
from trie.schemas.base import not_empty


class RolesSchema(BaseSchema):

    id = fields.UUID(dump_only=True)
    name = fields.String(required=True, validate=not_empty)
    description = fields.String(required=True, validate=not_empty)

    class Meta:
        type_ = 'roles'
        strict = True
