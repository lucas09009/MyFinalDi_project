"""empty message

Revision ID: 2f9e9817334d
Revises: f095548558c2
Create Date: 2023-12-27 15:53:29.132142

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f9e9817334d'
down_revision = 'f095548558c2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('articles', schema=None) as batch_op:
        batch_op.alter_column('details',
               existing_type=sa.TEXT(),
               type_=sa.String(length=180),
               existing_nullable=False)

    with op.batch_alter_table('usersdata', schema=None) as batch_op:
        batch_op.alter_column('Biographie',
               existing_type=sa.TEXT(),
               type_=sa.String(length=80),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usersdata', schema=None) as batch_op:
        batch_op.alter_column('Biographie',
               existing_type=sa.String(length=80),
               type_=sa.TEXT(),
               existing_nullable=True)

    with op.batch_alter_table('articles', schema=None) as batch_op:
        batch_op.alter_column('details',
               existing_type=sa.String(length=180),
               type_=sa.TEXT(),
               existing_nullable=False)

    # ### end Alembic commands ###
