from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy_utils import PasswordType

from trie.models.base import Base


class User(Base):

    email = Column(String)
    password = Column(PasswordType)
