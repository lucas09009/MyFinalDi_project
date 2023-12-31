"""empty message

Revision ID: da00ca90ba88
Revises: 17e7644b025f
Create Date: 2023-12-18 18:05:33.597327

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da00ca90ba88'
down_revision = '17e7644b025f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('UserViewArticles',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name_of_viewer', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('icon_name', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('promotions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nom_de_la_promotion', sa.String(), nullable=False),
    sa.Column('duree_de_la_promo', sa.Integer(), nullable=False),
    sa.Column('reduction', sa.Integer(), nullable=False),
    sa.Column('details', sa.Text(), nullable=True),
    sa.Column('image', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('usersdata',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('Image', sa.String(), nullable=True),
    sa.Column('Biographie', sa.String(length=80), nullable=True),
    sa.Column('Username', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('Password', sa.String(), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('Username'),
    sa.UniqueConstraint('email')
    )
    op.create_table('articles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=12), nullable=False),
    sa.Column('Description', sa.String(length=30), nullable=False),
    sa.Column('date_arrive', sa.Date(), nullable=False),
    sa.Column('details', sa.String(length=80), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('image', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(), nullable=True),
    sa.Column('user_image', sa.String(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('promotion_id', sa.Integer(), nullable=True),
    sa.Column('nombre_de_vues', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.ForeignKeyConstraint(['promotion_id'], ['promotions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('payement',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('prix_total', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['usersdata.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('articlesfavoris',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_of_user', sa.Integer(), nullable=True),
    sa.Column('id_of_article', sa.Integer(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('Username', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_of_article'], ['articles.id'], ),
    sa.ForeignKeyConstraint(['id_of_user'], ['usersdata.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('commentaires',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('commentaires', sa.Text(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('user_name', sa.String(), nullable=True),
    sa.Column('image', sa.String(), nullable=True),
    sa.Column('article_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['article_id'], ['articles.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['usersdata.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('panier',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('quantite', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('article_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['article_id'], ['articles.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['usersdata.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('association',
    sa.Column('article_id', sa.Integer(), nullable=True),
    sa.Column('panier_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['article_id'], ['articles.id'], ),
    sa.ForeignKeyConstraint(['panier_id'], ['panier.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('association')
    op.drop_table('panier')
    op.drop_table('commentaires')
    op.drop_table('articlesfavoris')
    op.drop_table('payement')
    op.drop_table('articles')
    op.drop_table('usersdata')
    op.drop_table('promotions')
    op.drop_table('category')
    op.drop_table('UserViewArticles')
    # ### end Alembic commands ###
