"""empty message

Revision ID: ea71ce14abd7
Revises: fe2515f4d878
Create Date: 2023-08-30 14:26:58.448986

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea71ce14abd7'
down_revision = 'fe2515f4d878'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('panier', schema=None) as batch_op:
        batch_op.add_column(sa.Column('article_id', sa.Integer(), nullable=True))
        batch_op.alter_column('quantite',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.create_foreign_key(None, 'articles', ['article_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('panier', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.alter_column('quantite',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.drop_column('article_id')

    # ### end Alembic commands ###
