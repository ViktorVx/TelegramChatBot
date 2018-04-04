"""add telegram_id column to user table

Revision ID: 27126c22f62f
Revises: ff8673e1423a
Create Date: 2018-04-04 07:24:01.257299

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27126c22f62f'
down_revision = 'ff8673e1423a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('telegram_user_id', sa.Integer))
    op.create_unique_constraint(None, 'user', ['telegram_user_id'])


def downgrade():
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_column('user', 'telegram_user_id')
