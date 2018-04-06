"""alter user_id colunm for autoincrement

Revision ID: ef9b0b364e27
Revises: 27126c22f62f
Create Date: 2018-04-04 20:20:52.096476

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef9b0b364e27'
down_revision = '27126c22f62f'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('user', 'id', autoincrement=True)


def downgrade():
    op.alter_column('user', 'id', autoincrement=False)
