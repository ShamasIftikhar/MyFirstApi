"""empty message

Revision ID: 47c5a723da23
Revises: 3368d3bce416
Create Date: 2022-01-02 09:18:11.762818

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47c5a723da23'
down_revision = '3368d3bce416'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('posts_users_fk', 'posts', type_='foreignkey')
    op.drop_column('posts', 'owner_email')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('owner_email', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.create_foreign_key('posts_users_fk', 'posts', 'users', ['owner_email'], ['email'], ondelete='CASCADE')
    # ### end Alembic commands ###