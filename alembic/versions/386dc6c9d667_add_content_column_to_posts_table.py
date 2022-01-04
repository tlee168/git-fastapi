"""add content column to posts table

Revision ID: 386dc6c9d667
Revises: 00796334584f
Create Date: 2022-01-04 11:03:16.793667

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '386dc6c9d667'
down_revision = '00796334584f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
