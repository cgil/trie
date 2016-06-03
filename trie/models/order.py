import sqlalchemy as sa
from sqlalchemy_utils import UUIDType

from trie import db
from trie.models.base import Base


class Order(Base):

    financial_status = sa.Column(sa.String)
    fulfillment_status = sa.Column(sa.String)
    total_price = sa.Column(sa.Numeric)

    shipping_address_city = sa.Column(sa.String)
    shipping_address_country_code = sa.Column(sa.String)
    shipping_address_country = sa.Column(sa.String)
    shipping_address_1 = sa.Column(sa.String)
    shipping_address_zip = sa.Column(sa.String)
    shipping_name = sa.Column(sa.String)

    member_id = sa.Column(UUIDType, db.ForeignKey('member.id'), nullable=False)
    store_id = sa.Column(UUIDType, db.ForeignKey('store.id'), nullable=False)
