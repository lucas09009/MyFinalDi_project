"""empty message

Revision ID: 3da527a89e8b
Revises: edfb5fc781e0
Create Date: 2023-08-25 18:33:41.893162

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3da527a89e8b'
down_revision = 'edfb5fc781e0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('articles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_name', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'usersdata', ['user_name'], ['Username'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('articles', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('user_name')

    # ### end Alembic commands ###
