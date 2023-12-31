"""empty message

Revision ID: b25784ee1a8b
Revises: 285e4f3b7c3a
Create Date: 2023-08-28 09:19:41.697614

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b25784ee1a8b'
down_revision = '285e4f3b7c3a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('articles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category', sa.String(), nullable=False))
        batch_op.drop_column('category_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('articles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_column('category')

    # ### end Alembic commands ###
