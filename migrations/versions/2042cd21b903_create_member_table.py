"""create member table

Revision ID: 2042cd21b903
Revises:
Create Date: 2016-05-15 09:05:02.425561

"""

# revision identifiers, used by Alembic.
revision = '2042cd21b903'
down_revision = None
branch_labels = None
depends_on = None

from uuid import uuid4

from alembic import op
import sqlalchemy as sa

from sqlalchemy_utils import PasswordType
from sqlalchemy_utils import UUIDType


def upgrade():
    op.create_table(
        'member',
        sa.Column(
            'id', UUIDType, primary_key=True, default=str(uuid4())
        ),
        sa.Column(
            'created_at',
            sa.DateTime,
            nullable=False,
            server_default=sa.text('now()'),
            default=sa.text('now()')
        ),
        sa.Column('deleted_at', sa.DateTime),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', PasswordType, nullable=False),
        sa.Column(
            'updated_at', sa.DateTime, nullable=False,
            server_onupdate=sa.text('now()'),
            onupdate=sa.text('now()'),
            default=sa.text('now()')
        ),
    )


def downgrade():
    op.drop_table('member')
