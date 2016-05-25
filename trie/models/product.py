from sqlalchemy import Column
from sqlalchemy import Numeric
from sqlalchemy import String

from trie.models.base import Base


class Product(Base):

    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    image = Column(String, nullable=False)
    price = Column(Numeric, nullable=False)

    def __init__(self, title, description, image, price):
        self.title = title
        self.description = description
        self.image = image
        self.price = price
