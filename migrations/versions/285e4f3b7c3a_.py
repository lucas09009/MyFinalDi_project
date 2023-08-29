"""empty message

Revision ID: 285e4f3b7c3a
Revises: dc706a3e48cf
Create Date: 2023-08-28 09:17:01.951726

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '285e4f3b7c3a'
down_revision = 'dc706a3e48cf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('category')
    with op.batch_alter_table('articles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category', sa.String(), nullable=False))
        batch_op.drop_constraint('articles_category_id_fkey', type_='foreignkey')
        batch_op.drop_column('category_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('articles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.create_foreign_key('articles_category_id_fkey', 'category', ['category_id'], ['id'])
        batch_op.drop_column('category')

    op.create_table('category',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('icon_name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='category_pkey')
    )
    # ### end Alembic commands ###