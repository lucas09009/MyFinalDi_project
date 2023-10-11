"""empty message

Revision ID: a39225230b86
Revises: 1c2a70d8c7db
Create Date: 2023-09-10 22:09:23.371926

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a39225230b86'
down_revision = '1c2a70d8c7db'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category_promo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('promo_name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('category_promo')
    # ### end Alembic commands ###