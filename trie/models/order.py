import sqlalchemy as sa
from sqlalchemy_utils import UUIDType

from trie import db
from trie.models.base import Base


class Order(Base):

    financial_status = sa.Column(sa.String, nullable=False)
    fulfillment_status = sa.Column(sa.String)
    total_price = sa.Column(sa.Numeric)

    member_id = sa.Column(UUIDType, db.ForeignKey('member.id'), nullable=False)
    store_id = sa.Column(UUIDType, db.ForeignKey('store.id'), nullable=False)
