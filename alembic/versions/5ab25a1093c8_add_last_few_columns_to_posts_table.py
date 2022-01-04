"""add last few columns to posts table

Revision ID: 5ab25a1093c8
Revises: 14d98cfaf34b
Create Date: 2022-01-04 11:59:25.950852

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ab25a1093c8'
down_revision = '14d98cfaf34b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False,
                    server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, 
                    server_default=sa.text('NOW()')))
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
