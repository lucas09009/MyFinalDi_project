"""empty message

Revision ID: bfe24b4cc58a
Revises: 2f9e9817334d
Create Date: 2023-12-27 16:42:35.045371

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bfe24b4cc58a'
down_revision = '2f9e9817334d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('articles', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=12),
               type_=sa.String(length=22),
               existing_nullable=False)
        batch_op.alter_column('details',
               existing_type=sa.VARCHAR(length=80),
               type_=sa.String(length=180),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('articles', schema=None) as batch_op:
        batch_op.alter_column('details',
               existing_type=sa.String(length=180),
               type_=sa.VARCHAR(length=80),
               existing_nullable=False)
        batch_op.alter_column('name',
               existing_type=sa.String(length=22),
               type_=sa.VARCHAR(length=12),
               existing_nullable=False)

    # ### end Alembic commands ###
