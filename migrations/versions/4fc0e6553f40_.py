"""empty message

Revision ID: 4fc0e6553f40
Revises: 3f3b2881d752
Create Date: 2023-09-03 11:19:13.474349

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4fc0e6553f40'
down_revision = '3f3b2881d752'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('promotions', schema=None) as batch_op:
        batch_op.alter_column('duree_de_la_promo',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('promotions', schema=None) as batch_op:
        batch_op.alter_column('duree_de_la_promo',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               existing_nullable=False)

    # ### end Alembic commands ###
