import datetime
import uuid

from flask import abort
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy.orm import ColumnProperty
from sqlalchemy.orm import class_mapper
from sqlalchemy_utils import UUIDType

from trie.database import db


class Base(db.Model):

    __abstract__ = True

    id = Column(UUIDType, default=lambda: uuid.uuid4().hex, primary_key=True)
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

    def __init__(self, **kwargs):
        # Remove invalid keys.
        for k in kwargs.iterkeys():
            if k not in self.columns():
                del kwargs[k]
        super(Base, self).__init__(**kwargs)

    def columns(self):
        """Get all model columns."""
        return [prop.key for prop in class_mapper(self.__class__).iterate_properties
                if isinstance(prop, ColumnProperty)]

    def save(self, resource):
        """Save to the database."""
        db.session.add(resource)
        return self.update()

    def update(self):
        """Updates the database records."""
        return db.session.commit()

    def delete(self, resource, soft_delete=True):
        """Delete a resource."""
        # Soft delete the resource by updating the deleted_at field.
        if soft_delete:
            resource.deleted_at = datetime.datetime.utcnow()
            return self.update()
        # Otherwise, permanently delete a resource.
        db.session.delete(resource)
        return db.session.commit()

    @classmethod
    def get_all(cls):
        """Get all records."""
        return cls.query.filter(
            cls.deleted_at.is_(None)
        ).all()

    @classmethod
    def get(cls, record_id):
        """Get a record."""
        return cls.query.filter(
            cls.id == record_id
        ).filter(
            cls.deleted_at.is_(None)
        ).first()

    @classmethod
    def get_or_404(cls, record_id):
        """Get a record or 404."""
        record = cls.query.filter(
            cls.id == record_id
        ).filter(
            cls.deleted_at.is_(None)
        ).first()
        return record or abort(404)
