"""empty message

Revision ID: d7a0149ad7a4
Revises: ccbb95bc2456
Create Date: 2023-09-03 11:25:55.465245

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd7a0149ad7a4'
down_revision = 'ccbb95bc2456'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('promotions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('articleId', sa.String(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('promotions', schema=None) as batch_op:
        batch_op.drop_column('articleId')

    # ### end Alembic commands ###
