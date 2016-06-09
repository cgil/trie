from flask.ext.security import UserMixin
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy_utils import UUIDType

from trie.lib.database import db
from trie.lib.secure import security
from trie.models.base import Base
from trie.utils.configuration import config

roles_members = db.Table(
    'roles_members',
    Column('member_id', UUIDType, db.ForeignKey('member.id')),
    Column('role_id', UUIDType, db.ForeignKey('role.id'))
)


class Member(Base, UserMixin):

    """A member of our platform."""

    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    stripe_customer_id = Column(String)
    active = Column(Boolean, default=True)
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

    def __init__(self, **kwargs):
        super(Member, self).__init__(**kwargs)
        roles = kwargs.get('roles') or [config.get('roles.default_role')]
        for role in roles:
            if isinstance(role, str):
                member_role = security.datastore.find_role(role)
            else:
                member_role = role
            security.datastore.add_role_to_user(self, member_role)

    @classmethod
    def private_fields(cls):
        """Fields that should be private and never exposed."""
        return (
            'active',
            'confirmed_at',
            'created_at',
            'current_login_at',
            'current_login_ip',
            'deleted_at',
            'last_login_at',
            'last_login_ip',
            'login_count',
            'password',
            'stripe_customer_id',
            'updated_at',
            'roles',
        )

    @classmethod
    def get_by_email(cls, email):
        """Returns a member by email."""
        return cls.query.filter(
            cls.email == email
        ).filter(
            cls.deleted_at.is_(None)
        ).first()
