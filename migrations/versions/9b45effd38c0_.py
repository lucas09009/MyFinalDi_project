"""empty message

Revision ID: 9b45effd38c0
Revises: c5f1524cbfa0
Create Date: 2023-08-21 10:15:33.901866

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b45effd38c0'
down_revision = 'c5f1524cbfa0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('articles', schema=None) as batch_op:
        batch_op.drop_constraint('articles_name_key', type_='unique')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('articles', schema=None) as batch_op:
        batch_op.create_unique_constraint('articles_name_key', ['name'])

    # ### end Alembic commands ###
