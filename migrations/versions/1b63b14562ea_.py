"""empty message

Revision ID: 1b63b14562ea
Revises: 8a4fa6236e94
Create Date: 2023-08-30 09:22:28.748078

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b63b14562ea'
down_revision = '8a4fa6236e94'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('promotion')
    with op.batch_alter_table('panier', schema=None) as batch_op:
        batch_op.drop_constraint('panier_user_id_fkey', type_='foreignkey')
        batch_op.drop_column('user_id')

    with op.batch_alter_table('usersdata', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_panier', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'panier', ['user_panier'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usersdata', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('user_panier')

    with op.batch_alter_table('panier', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('panier_user_id_fkey', 'usersdata', ['user_id'], ['id'])

    op.create_table('promotion',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id', name='promotion_pkey')
    )
    # ### end Alembic commands ###
