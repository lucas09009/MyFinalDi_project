"""empty message

Revision ID: e2e6d9e4b7b3
Revises: 9dffc661dab7
Create Date: 2023-08-15 13:04:31.987190

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2e6d9e4b7b3'
down_revision = '9dffc661dab7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usersdata', schema=None) as batch_op:
        batch_op.add_column(sa.Column('inscription_time', sa.DateTime(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usersdata', schema=None) as batch_op:
        batch_op.drop_column('inscription_time')

    # ### end Alembic commands ###
