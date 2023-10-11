"""empty message

Revision ID: 130e16ec3760
Revises: 2bd5f07136ab
Create Date: 2023-09-04 21:23:39.212183

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '130e16ec3760'
down_revision = '2bd5f07136ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Commentaires',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name_of_viewer', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Commentaires')
    # ### end Alembic commands ###