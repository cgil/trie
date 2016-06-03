"""create orders table

Revision ID: 2b72887a1de5
Revises: d2549ba843ac
Create Date: 2016-06-03 10:05:10.870791

"""

# revision identifiers, used by Alembic.
revision = '2b72887a1de5'
down_revision = 'd2549ba843ac'

from uuid import uuid4

from alembic import op
import sqlalchemy as sa
from sqlalchemy_utils import UUIDType


def upgrade():
    op.create_table(
        'order',
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
        sa.Column('financial_status', sa.String(), nullable=False),
        sa.Column('fulfillment_status', sa.String()),
        sa.Column('total_price', sa.Numeric(), nullable=False),
        sa.Column('shipping_address_city', sa.String()),
        sa.Column('shipping_address_country', sa.String()),
        sa.Column('shipping_address_country_code', sa.String()),
        sa.Column('shipping_address_1', sa.String()),
        sa.Column('shipping_address_zip', sa.String()),
        sa.Column('shipping_name', sa.String()),

        sa.Column('member_id', UUIDType),
        sa.Column('store_id', UUIDType),
    )


def downgrade():
    op.drop_table('order')
