"""add stripe_customer_id column to members

Revision ID: 783f66cd8424
Revises: 2b72887a1de5
Create Date: 2016-06-03 10:37:38.591948

"""

# revision identifiers, used by Alembic.
revision = '783f66cd8424'
down_revision = '2b72887a1de5'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('member', sa.Column('stripe_customer_id', sa.String()))


def downgrade():
    op.drop_column('member', 'stripe_customer_id')
