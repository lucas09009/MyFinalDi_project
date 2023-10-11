"""empty message

Revision ID: 20ee86dc855b
Revises: 2aafc3fde5d5
Create Date: 2023-09-03 11:27:20.889911

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20ee86dc855b'
down_revision = '2aafc3fde5d5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('promotions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('articleId', sa.Integer(), nullable=False),
    sa.Column('duree_de_la_promo', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('articles', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'promotions', ['promotion_article_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('articles', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    op.drop_table('promotions')
    # ### end Alembic commands ###