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

    def __eq__(self, other):
        """Checks the equality of two Member objects using `get_id`."""
        return self.get_id() == other.get_id()

    def __ne__(self, other):
        """Checks the inequality of two Member objects using `get_id`."""
        return not self.__eq__(other)

    @property
    def is_authenticated(self):
        """Check if the member is authenticated."""
        return True

    @property
    def is_active(self):
        """Check if the member's account is active, and not suspended."""
        return True

    @property
    def is_anonymous(self):
        """Check if this is an anonymous member (guest)."""
        return False

    @classmethod
    def get_known_member(cls, email, password):
        """Check if we can authenticate a known member."""
        found = cls.query.filter_by(
            email=email,
        ).first()
        if not found:
            return None
        if found.password == password:
            return found

    @classmethod
    def email_exists(cls, email):
        """Check if the email already exists."""
        found = cls.query.filter_by(
            email=email,
        ).first()
        return True if found else False

    def get_id(self):
        """Returns the id of this member."""
        return self.id
