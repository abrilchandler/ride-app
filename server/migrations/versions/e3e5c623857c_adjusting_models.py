"""adjusting models

Revision ID: e3e5c623857c
Revises: 0cc7714b2314
Create Date: 2025-01-07 15:02:47.337761

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e3e5c623857c'
down_revision = '0cc7714b2314'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_ride')
    with op.batch_alter_table('bookings', schema=None) as batch_op:
        batch_op.drop_column('feedback')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bookings', schema=None) as batch_op:
        batch_op.add_column(sa.Column('feedback', sa.VARCHAR(length=500), nullable=True))

    op.create_table('user_ride',
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('ride_id', sa.INTEGER(), nullable=False),
    sa.Column('status', sa.VARCHAR(), nullable=False),
    sa.ForeignKeyConstraint(['ride_id'], ['rides.id'], name='fk_user_ride_ride_id_rides'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_user_ride_user_id_users'),
    sa.PrimaryKeyConstraint('user_id', 'ride_id')
    )
    # ### end Alembic commands ###
