"""add security fields to member table

Revision ID: f580e944c99f
Revises: c5b44fdcd4c5
Create Date: 2016-06-08 17:22:12.961146

"""

# revision identifiers, used by Alembic.
revision = 'f580e944c99f'
down_revision = 'c5b44fdcd4c5'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('member', sa.Column('active', sa.Boolean()))
    op.add_column('member', sa.Column('confirmed_at', sa.DateTime()))
    op.add_column('member', sa.Column('current_login_at', sa.DateTime()))
    op.add_column('member', sa.Column('current_login_ip', sa.String()))
    op.add_column('member', sa.Column('last_login_at', sa.DateTime()))
    op.add_column('member', sa.Column('last_login_ip', sa.String()))
    op.add_column('member', sa.Column('login_count', sa.Integer()))


def downgrade():
    op.drop_column('member', 'active')
    op.drop_column('member', 'confirmed_at')
    op.drop_column('member', 'current_login_at')
    op.drop_column('member', 'current_login_ip')
    op.drop_column('member', 'last_login_at')
    op.drop_column('member', 'last_login_ip')
    op.drop_column('member', 'login_count')
