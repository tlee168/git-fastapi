"""create posts table

Revision ID: 00796334584f
Revises: 
Create Date: 2022-01-04 09:55:39.367373

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00796334584f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("posts", sa.Column('id', sa.Integer(), nullable=False, primary_key=True ),
        sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
