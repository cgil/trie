"""add store_id column

Revision ID: d2549ba843ac
Revises: 935a98d2fd2b
Create Date: 2016-06-01 17:57:59.390055

"""

# revision identifiers, used by Alembic.
revision = 'd2549ba843ac'
down_revision = '935a98d2fd2b'

from alembic import op
import sqlalchemy as sa

from sqlalchemy_utils import UUIDType


def upgrade():
    op.add_column('product', sa.Column('store_id', UUIDType, nullable=True))


def downgrade():
    op.drop_column('product', 'store_id')
