from flask.ext.security import RoleMixin
from sqlalchemy import Column
from sqlalchemy import String

from trie.models.base import Base


class Role(Base, RoleMixin):

    """A member role for authentication and authorization."""

    name = Column(String, unique=True, nullable=False)
    description = Column(String, unique=True, nullable=False)
