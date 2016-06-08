"""alter column member password to string

Revision ID: bde1bd927de6
Revises: 020d8a2c958f
Create Date: 2016-06-08 21:43:48.569138

"""

# revision identifiers, used by Alembic.
revision = 'bde1bd927de6'
down_revision = '020d8a2c958f'

from alembic import op
import sqlalchemy as sa
from sqlalchemy_utils import PasswordType


def upgrade():
    op.alter_column('member', 'password', type_=sa.String())


def downgrade():
    op.alter_column('member', 'password', type_=PasswordType)
