import datetime
import uuid

from sqlalchemy import Column
from sqlalchemy import DateTime
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
