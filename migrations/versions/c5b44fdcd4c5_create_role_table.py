"""create role table

Revision ID: c5b44fdcd4c5
Revises: 86f3d142b8de
Create Date: 2016-06-08 16:37:07.429784

"""

# revision identifiers, used by Alembic.
revision = 'c5b44fdcd4c5'
down_revision = '86f3d142b8de'

from uuid import uuid4

from alembic import op
import sqlalchemy as sa
from sqlalchemy_utils import UUIDType


def upgrade():
    op.create_table(
        'role',
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
        sa.Column(
            'updated_at', sa.DateTime, nullable=False,
            server_onupdate=sa.text('now()'),
            onupdate=sa.text('now()'),
            default=sa.text('now()')
        ),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
    )


def downgrade():
    op.drop_table('role')
