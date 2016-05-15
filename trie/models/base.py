from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql import text
from sqlalchemy_utils import UUIDType

from app import db
from trie.utils.convert import camel_case_to_snake_case


class Base(db):

    @declared_attr
    def __tablename__(cls):
        return camel_case_to_snake_case(cls.__name__)

    id = Column(UUIDType, server_default=text('uuid_generate_v4()'), primary_key=True)
    created_at = Column(DateTime, server_default=db.func.now(), required=True)
    deleted_at = Column(DateTime)
    updated_at = Column(
        DateTime, server_default=db.func.now(), onupdate=db.func.now(), required=True
    )


Base = declarative_base(cls=Base)
