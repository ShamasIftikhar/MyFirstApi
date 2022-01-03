"""add foriegn-key to posts table

Revision ID: 2bdcb30a519e
Revises: 84f6e9f1ba1d
Create Date: 2022-01-01 10:01:32.834257

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2bdcb30a519e'
down_revision = '84f6e9f1ba1d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column(
        "owner_email", sa.String(), nullable=False,))
    op.create_foreign_key("posts_users_fk", source_table="posts", referent_table="users", local_cols=[
                          'owner_email'], remote_cols=['email'], ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint("posts_users_fk",table_name="posts")
    op.drop_column("posts","owner_id")
    pass
