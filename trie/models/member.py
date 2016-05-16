from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy_utils import PasswordType

from trie.models.base import Base


class Member(Base):

    email = Column(String, unique=True, nullable=False)
    password = Column(PasswordType(
        schemes=[
            'sha256_crypt',
        ]
    ), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return '<Member %r>' % self.email

    @classmethod
    def does_authenticate(cls, email, password):
        """Check if we can authenticate a member."""
        found = cls.query.filter_by(
            email=email,
            password=password,
        ).first()
        return True if found else False

    @classmethod
    def email_exists(cls, email):
        """Check if the email already exists."""
        found = cls.query.filter_by(
            email=email,
        ).first()
        return True if found else False
