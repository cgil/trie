"""create roles_members table

Revision ID: 020d8a2c958f
Revises: f580e944c99f
Create Date: 2016-06-08 21:24:25.074582

"""

# revision identifiers, used by Alembic.
revision = '020d8a2c958f'
down_revision = 'f580e944c99f'

from alembic import op
import sqlalchemy as sa
from sqlalchemy_utils import UUIDType


def upgrade():
    op.create_table(
        'roles_members',
        sa.Column('role_id', UUIDType),
        sa.Column('member_id', UUIDType),
    )


def downgrade():
    op.drop_table('roles_members')
