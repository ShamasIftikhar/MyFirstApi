"""create users table

Revision ID: 84f6e9f1ba1d
Revises: 1aa9b216cb26
Create Date: 2022-01-01 09:41:44.099867

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.schema import Column, PrimaryKeyConstraint
from sqlalchemy.sql.sqltypes import String


# revision identifiers, used by Alembic.
revision = '84f6e9f1ba1d'
down_revision = '1aa9b216cb26'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users", sa.Column("id", sa.Integer(), nullable=False), sa.Column(
        "email", sa.String(), nullable=False), sa.Column("password", sa.String(), nullable=False), sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),sa.PrimaryKeyConstraint('id'),sa.UniqueConstraint('email'))
    pass


def downgrade():
    op.drop_table('users')
    pass
