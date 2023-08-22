"""empty message

Revision ID: 8ea7db90f60f
Revises: f51f988e8959
Create Date: 2023-08-21 21:52:55.124609

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ea7db90f60f'
down_revision = 'f51f988e8959'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('association',
    sa.Column('article_id', sa.Integer(), nullable=True),
    sa.Column('panier_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['article_id'], ['articles.id'], ),
    sa.ForeignKeyConstraint(['panier_id'], ['panier.id'], )
    )
    op.drop_table('articles_paniers')
    with op.batch_alter_table('panier', schema=None) as batch_op:
        batch_op.drop_constraint('panier_article_id_fkey', type_='foreignkey')
        batch_op.drop_column('article_id')

    with op.batch_alter_table('usersdata', schema=None) as batch_op:
        batch_op.drop_constraint('usersdata_panier_id_key', type_='unique')
        batch_op.drop_constraint('usersdata_panier_id_fkey', type_='foreignkey')
        batch_op.drop_column('panier_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usersdata', schema=None) as batch_op:
        batch_op.add_column(sa.Column('panier_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('usersdata_panier_id_fkey', 'panier', ['panier_id'], ['id'])
        batch_op.create_unique_constraint('usersdata_panier_id_key', ['panier_id'])

    with op.batch_alter_table('panier', schema=None) as batch_op:
        batch_op.add_column(sa.Column('article_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.create_foreign_key('panier_article_id_fkey', 'articles', ['article_id'], ['id'], ondelete='SET NULL')

    op.create_table('articles_paniers',
    sa.Column('article_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('panier_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['article_id'], ['articles.id'], name='articles_paniers_article_id_fkey'),
    sa.ForeignKeyConstraint(['panier_id'], ['panier.id'], name='articles_paniers_panier_id_fkey'),
    sa.PrimaryKeyConstraint('article_id', 'panier_id', name='articles_paniers_pkey')
    )
    op.drop_table('association')
    # ### end Alembic commands ###
