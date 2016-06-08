from flask.ext.security import UserMixin
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy_utils import PasswordType
from sqlalchemy_utils import UUIDType

from trie import db
from trie.models.base import Base

roles_members = db.Table(
    'roles_members',
    db.Column('member_id', UUIDType, db.ForeignKey('member.id')),
    db.Column('role_id', UUIDType, db.ForeignKey('role.id'))
)


class Member(Base, UserMixin):

    """A member of our platform."""

    email = Column(String, unique=True, nullable=False)
    password = Column(PasswordType(
        schemes=[
            'sha512_crypt',
        ]
    ), nullable=False)
    stripe_customer_id = Column(String)
    active = Column(Boolean)
    confirmed_at = Column(DateTime)
    current_login_at = Column(DateTime)
    current_login_ip = Column(String)
    last_login_at = Column(db.DateTime)
    last_login_ip = Column(String)
    login_count = Column(Integer)

    orders = db.relationship('Order', backref='member', lazy='dynamic')
    roles = db.relationship(
        'Role', secondary=roles_members, backref='member', lazy='dynamic'
    )

    def __repr__(self):
        return '<Member %r>' % self.email

    @property
    def private_fields(self):
        """Fields that should be private and never exposed."""
        return (
            'created_at',
            'updated_at',
            'deleted_at',
            'password',
            'stripe_customer_id',
            'active',
            'confirmed_at',
            'current_login_at',
            'current_login_ip',
            'last_login_at',
            'last_login_ip',
            'login_count',
        )

    @classmethod
    def get_by_email(cls, email):
        """Returns a member by email."""
        return cls.query.filter(
            cls.email == email
        ).filter(
            cls.deleted_at.is_(None)
        ).first()
