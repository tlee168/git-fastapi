"""add foreign key to posts table

Revision ID: 14d98cfaf34b
Revises: bb8df4f0b7a1
Create Date: 2022-01-04 11:27:21.496876

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '14d98cfaf34b'
down_revision = 'bb8df4f0b7a1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts",
            referent_table="users", local_cols=['owner_id'], remote_cols=['id'],
            ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
