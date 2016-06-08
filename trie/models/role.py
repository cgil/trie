from flask.ext.security import RoleMixin
from sqlalchemy import Column
from sqlalchemy import String

from trie import security
from trie.models.base import Base


class Role(Base, RoleMixin):

    """A member role for authentication and authorization."""

    name = Column(String, unique=True, nullable=False)
    description = Column(String, unique=True, nullable=False)

    def __init__(self, **kwargs):
        # Remove invalid keys.
        name = kwargs.pop('name')
        for k in kwargs.keys():
            if k not in self.columns():
                del kwargs[k]

        role = security.datastore.find_or_create_role(name, **kwargs)
        return role
