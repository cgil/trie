"""create store table

Revision ID: 935a98d2fd2b
Revises: ba1f57ef7cc6
Create Date: 2016-06-01 10:24:01.185935

"""

# revision identifiers, used by Alembic.
revision = '935a98d2fd2b'
down_revision = 'ba1f57ef7cc6'

from uuid import uuid4

from alembic import op
import sqlalchemy as sa

from sqlalchemy_utils import UUIDType


def upgrade():
    op.create_table(
        'store',
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
        sa.Column('tote_domain', sa.String(), nullable=False),
        sa.Column('domain', sa.String()),
        sa.Column('email', sa.String()),
        sa.Column('address_1', sa.String()),
        sa.Column('city', sa.String()),
        sa.Column('zip_code', sa.String()),
        sa.Column('country', sa.String()),
        sa.Column('country_code', sa.String()),
        sa.Column('currency', sa.String()),
        sa.Column('phone', sa.String()),
    )


def downgrade():
    op.drop_table('store')
