"""add user action type column and type

Revision ID: 2ab6c357d370
Revises: 525cfd735a69
Create Date: 2018-04-15 12:09:50.425357

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM


# revision identifiers, used by Alembic.
revision = '2ab6c357d370'
down_revision = '525cfd735a69'
branch_labels = None
depends_on = None

user_action_type = ENUM('main_menu', 'date_input', 'time_input', name='useractiontype', create_type=True)

def upgrade():
    user_action_type.create(op.get_bind(), checkfirst=True)
    op.add_column('user', sa.Column('user_action', user_action_type))


def downgrade():
    op.drop_column('user', 'user_action')
