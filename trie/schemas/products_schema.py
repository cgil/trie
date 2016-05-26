from marshmallow import fields

from trie.schemas.base import BaseSchema
from trie.schemas.base import not_empty


class ProductsSchema(BaseSchema):

    id = fields.Integer(dump_only=True)
    description = fields.String(required=True, validate=not_empty)
    image = fields.String(required=True, validate=not_empty)
    price = fields.Decimal(required=True, validate=not_empty)
    title = fields.String(required=True, validate=not_empty)

    # self links
    def get_top_level_links(self, data, many):
        if many:
            self_link = "/products/"
        else:
            self_link = "/products/{}".format(data['id'])
        return {'self': self_link}

    class Meta:
        type_ = 'products'
