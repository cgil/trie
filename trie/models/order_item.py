import sqlalchemy as sa
from sqlalchemy_utils import UUIDType

from trie import db
from trie.models.base import Base


class OrderItem(Base):

    """A list item in an order."""

    member_id = sa.Column(UUIDType, db.ForeignKey('member.id'), nullable=False)
    order_id = sa.Column(UUIDType, db.ForeignKey('order.id'), nullable=False)
    product_id = sa.Column(UUIDType, db.ForeignKey('product.id'), nullable=False)
    store_id = sa.Column(UUIDType, db.ForeignKey('store.id'), nullable=False)
    quantity = sa.Column(sa.Numeric, nullable=False)
