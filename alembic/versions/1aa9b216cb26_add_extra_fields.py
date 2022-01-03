"""add extra fields

Revision ID: 1aa9b216cb26
Revises: f08acf3d086c
Create Date: 2022-01-01 09:22:50.673811

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import nullslast


# revision identifiers, used by Alembic.
revision = '1aa9b216cb26'
down_revision = 'f08acf3d086c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("published", sa.Boolean(),
                  nullable=False, server_default="TRUE"))
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(
        timezone=True), nullable=False, server_default=sa.text('now()')))
    pass


def downgrade():
    op.drop_column("posts","content=")
    op.drop_column("posts","created_at")
    pass
