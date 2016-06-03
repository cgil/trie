import sqlalchemy as sa

from trie import db
from trie.models.base import Base


class Store(Base):

    """An in-app store."""

    name = sa.Column(sa.String, nullable=False)
    tote_domain = sa.Column(sa.String, nullable=False, unique=True)
    domain = sa.Column(sa.String)
    email = sa.Column(sa.String)
    address_1 = sa.Column(sa.String)
    city = sa.Column(sa.String)
    zip_code = sa.Column(sa.String)
    country = sa.Column(sa.String)
    country_code = sa.Column(sa.String)
    currency = sa.Column(sa.String)
    phone = sa.Column(sa.String)

    products = db.relationship('Product', backref='store', lazy='dynamic')
    orders = db.relationship('Order', backref='store', lazy='dynamic')
