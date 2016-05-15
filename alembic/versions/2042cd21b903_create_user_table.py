"""create user table

Revision ID: 2042cd21b903
Revises:
Create Date: 2016-05-15 09:05:02.425561

"""

# revision identifiers, used by Alembic.
revision = '2042cd21b903'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

from sqlalchemy_utils import UUIDType


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', UUIDType, primary_key=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('deleted_at', sa.DateTime),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
    )


def downgrade():
    op.drop_table('user')
