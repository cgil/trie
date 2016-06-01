import sqlalchemy as sa
from sqlalchemy_utils import UUIDType

from trie import db
from trie.models.base import Base


class Product(Base):

    description = sa.Column(sa.String, nullable=False)
    image = sa.Column(sa.String, nullable=False)
    price = sa.Column(sa.Numeric, nullable=False)
    title = sa.Column(sa.String, nullable=False)

    store_id = db.Column(UUIDType, db.ForeignKey('store.id'))
