"""Donation update2

Revision ID: 7dff84ff9c8d
Revises: 0472c0aac201
Create Date: 2022-08-25 15:59:41.378469

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7dff84ff9c8d'
down_revision = '0472c0aac201'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('donation', schema=None) as batch_op:
        batch_op.drop_column('charityproject_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('donation', schema=None) as batch_op:
        batch_op.add_column(sa.Column('charityproject_id', sa.INTEGER(), nullable=True))
        batch_op.create_foreign_key(None, 'charityproject', ['charityproject_id'], ['id'])

    # ### end Alembic commands ###
