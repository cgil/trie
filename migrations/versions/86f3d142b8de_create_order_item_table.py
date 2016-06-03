"""create order item table

Revision ID: 86f3d142b8de
Revises: 783f66cd8424
Create Date: 2016-06-03 18:24:07.403778

"""

# revision identifiers, used by Alembic.
revision = '86f3d142b8de'
down_revision = '783f66cd8424'

from uuid import uuid4

from alembic import op
import sqlalchemy as sa
from sqlalchemy_utils import UUIDType


def upgrade():
    op.create_table(
        'order_item',
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
        sa.Column('quantity', sa.Numeric(), nullable=False),
        sa.Column('store_id', UUIDType),
        sa.Column('member_id', UUIDType),
        sa.Column('product_id', UUIDType),
        sa.Column('order_id', UUIDType),
    )


def downgrade():
    op.drop_table('order_item')
