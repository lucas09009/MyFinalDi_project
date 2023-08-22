"""empty message

Revision ID: a0f0ee2e8805
Revises: e6a2a92ff2b1
Create Date: 2023-08-21 21:24:04.035180

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0f0ee2e8805'
down_revision = 'e6a2a92ff2b1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('articles_paniers',
    sa.Column('article_id', sa.Integer(), nullable=False),
    sa.Column('panier_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['article_id'], ['articles.id'], ),
    sa.ForeignKeyConstraint(['panier_id'], ['panier.id'], ),
    sa.PrimaryKeyConstraint('article_id', 'panier_id')
    )
    op.drop_table('users_paniers')
    with op.batch_alter_table('panier', schema=None) as batch_op:
        batch_op.drop_constraint('panier_user_id_fkey', type_='foreignkey')
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('panier', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.create_foreign_key('panier_user_id_fkey', 'usersdata', ['user_id'], ['id'])

    op.create_table('users_paniers',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('panier_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['panier_id'], ['panier.id'], name='users_paniers_panier_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['usersdata.id'], name='users_paniers_user_id_fkey')
    )
    op.drop_table('articles_paniers')
    # ### end Alembic commands ###
