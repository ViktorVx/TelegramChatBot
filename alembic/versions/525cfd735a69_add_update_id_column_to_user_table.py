"""add update_id column to user table

Revision ID: 525cfd735a69
Revises: ef9b0b364e27
Create Date: 2018-04-08 08:37:24.458081

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '525cfd735a69'
down_revision = 'ef9b0b364e27'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('update_id', sa.Integer))


def downgrade():
    op.drop_column('user', 'update_id')
