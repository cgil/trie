from sqlalchemy import Column
from sqlalchemy import Numeric
from sqlalchemy import String

from trie.models.base import Base


class Product(Base):

    description = Column(String, nullable=False)
    image = Column(String, nullable=False)
    price = Column(Numeric, nullable=False)
    title = Column(String, nullable=False)

    def __init__(self, title=None, description=None, image=None, price=None):
        self.description = description
        self.image = image
        self.price = price
        self.title = title
