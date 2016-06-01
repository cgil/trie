import sqlalchemy as sa

from trie.models.base import Base


class Product(Base):

    description = sa.Column(sa.String, nullable=False)
    image = sa.Column(sa.String, nullable=False)
    price = sa.Column(sa.Numeric, nullable=False)
    title = sa.Column(sa.String, nullable=False)
