"""empty message

Revision ID: 570fa7df5ab7
Revises: 6649f23dc1b4
Create Date: 2024-03-21 15:50:11.838270

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '570fa7df5ab7'
down_revision = '6649f23dc1b4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('articles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(length=100), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('articles', schema=None) as batch_op:
        batch_op.drop_column('email')

    # ### end Alembic commands ###
