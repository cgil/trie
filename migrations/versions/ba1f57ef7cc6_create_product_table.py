"""create product table

Revision ID: ba1f57ef7cc6
Revises: 2042cd21b903
Create Date: 2016-05-25 16:06:51.715448

"""

# revision identifiers, used by Alembic.
revision = 'ba1f57ef7cc6'
down_revision = '2042cd21b903'

from uuid import uuid4

from alembic import op
import sqlalchemy as sa

from sqlalchemy_utils import UUIDType


def upgrade():
    op.create_table(
        'product',
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
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('image', sa.String(), nullable=False),
        sa.Column('price', sa.Numeric(), nullable=False),
    )


def downgrade():
    op.drop_table('product')
