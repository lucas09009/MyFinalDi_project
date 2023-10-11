"""empty message

Revision ID: 92743acabf2a
Revises: ca53a28ab038
Create Date: 2023-09-04 22:08:41.130743

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92743acabf2a'
down_revision = 'ca53a28ab038'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('UserViewArticles',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name_of_viewer', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('UserViewArticles')
    # ### end Alembic commands ###
