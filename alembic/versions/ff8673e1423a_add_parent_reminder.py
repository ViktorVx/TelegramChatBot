"""add parent_reminder

Revision ID: ff8673e1423a
Revises: 
Create Date: 2018-03-25 08:34:55.492633

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff8673e1423a'
down_revision = None
#branch_labels = None
#depends_on = None


def upgrade():
    op.add_column('reminder', sa.Column('parent_reminder_id', sa.Integer()))
    op.create_foreign_key(None, 'reminder', 'reminder', ['parent_reminder_id'], ['id'])


def downgrade():
    op.drop_column('reminder', 'parent_reminder_id')
