"""empty message

Revision ID: 06400449d4e5
Revises: a7667dc9c6ea
Create Date: 2023-09-05 09:33:29.997926

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06400449d4e5'
down_revision = 'a7667dc9c6ea'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('articlesfavoris',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('article_id', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('Username', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['article_id'], ['articles.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['usersdata.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('panier', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('article_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('panier', schema=None) as batch_op:
        batch_op.alter_column('article_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    op.drop_table('articlesfavoris')
    # ### end Alembic commands ###