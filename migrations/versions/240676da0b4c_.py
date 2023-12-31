"""empty message

Revision ID: 240676da0b4c
Revises: 55e21eb6ee7f
Create Date: 2023-09-08 20:57:07.103876

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '240676da0b4c'
down_revision = '55e21eb6ee7f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('promotions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('nom_de_la_promotion', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('reduction', sa.Integer(), nullable=False))
        batch_op.drop_column('articleId')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('promotions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('articleId', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_column('reduction')
        batch_op.drop_column('nom_de_la_promotion')

    # ### end Alembic commands ###
