"""init

Revision ID: 854b51d02838
Revises: 
Create Date: 2024-06-13 18:47:02.194552

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '854b51d02838'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fan',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('speed', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('sensor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('speed_reading',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fan_id', sa.Integer(), nullable=False),
    sa.Column('speed', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('change_reason', sa.String(length=64), nullable=False),
    sa.ForeignKeyConstraint(['fan_id'], ['fan.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('speed_reading', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_speed_reading_change_reason'), ['change_reason'], unique=False)
        batch_op.create_index(batch_op.f('ix_speed_reading_fan_id'), ['fan_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_speed_reading_timestamp'), ['timestamp'], unique=False)

    op.create_table('temp_reading',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sensor_id', sa.Integer(), nullable=False),
    sa.Column('temp', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['sensor_id'], ['sensor.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('temp_reading', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_temp_reading_sensor_id'), ['sensor_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_temp_reading_timestamp'), ['timestamp'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('temp_reading', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_temp_reading_timestamp'))
        batch_op.drop_index(batch_op.f('ix_temp_reading_sensor_id'))

    op.drop_table('temp_reading')
    with op.batch_alter_table('speed_reading', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_speed_reading_timestamp'))
        batch_op.drop_index(batch_op.f('ix_speed_reading_fan_id'))
        batch_op.drop_index(batch_op.f('ix_speed_reading_change_reason'))

    op.drop_table('speed_reading')
    op.drop_table('sensor')
    op.drop_table('fan')
    # ### end Alembic commands ###
