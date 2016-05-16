from uuid import uuid4

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_utils import UUIDType

from trie.database import db
from trie.utils.convert import camel_case_to_snake_case


class Base(object):

    @declared_attr
    def __tablename__(cls):
        return camel_case_to_snake_case(cls.__name__)

    id = Column(UUIDType, default=str(uuid4()), primary_key=True)
    created_at = Column(
        DateTime,
        server_default=db.func.now(),
        default=db.func.now()
    )
    deleted_at = Column(DateTime)
    updated_at = Column(
        DateTime,
        server_onupdate=db.func.now(),
        onupdate=db.func.now(),
        default=db.func.now()
    )

Base = declarative_base(cls=Base)
Base.query = db.session.query_property()
