"""create posts tablr

Revision ID: f08acf3d086c
Revises: 
Create Date: 2022-01-01 08:59:13.920112

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f08acf3d086c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column("id", sa.Integer(), nullable=False, primary_key=True), sa.Column(
        "title", sa.String(), nullable=False), sa.Column("content", sa.String(), nullable=False))


def downgrade():
    op.drop_table("posts")
