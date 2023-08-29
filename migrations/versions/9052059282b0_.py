"""empty message

Revision ID: 9052059282b0
Revises: 6fe604f3e7fd
Create Date: 2023-08-27 18:58:57.198328

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9052059282b0'
down_revision = '6fe604f3e7fd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('articles',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('Description', sa.String(), nullable=False),
    sa.Column('date_arrive', sa.Date(), nullable=False),
    sa.Column('details', sa.Text(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('image', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('user_name', sa.String(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['usersdata.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('association', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'articles', ['article_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('association', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    op.drop_table('articles')
    # ### end Alembic commands ###
