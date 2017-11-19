"""create regions and zones

Revision ID: ba75fca08593
Revises: 3ce1572cbc6b
Create Date: 2017-11-04 09:08:59.648307

"""
import sqlalchemy as sa
import sqlalchemy_utils as sau
from alembic import op

# revision identifiers, used by Alembic.
from ingredients_db.models.region import RegionState
from ingredients_db.models.zones import ZoneState

revision = 'ba75fca08593'
down_revision = '3ce1572cbc6b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'regions',
        sa.Column('id', sau.UUIDType, server_default=sa.text("uuid_generate_v4()"), primary_key=True),
        sa.Column('name', sa.String, unique=True, nullable=False),
        sa.Column('datacenter', sa.String, unique=True, nullable=False),
        sa.Column('image_datastore', sa.String, nullable=False),
        sa.Column('image_folder', sa.String),
        sa.Column('schedulable', sa.Boolean, nullable=False),

        sa.Column('state', sa.Enum(RegionState), default=RegionState.CREATING, nullable=False),
        sa.Column('current_task_id', sau.UUIDType, sa.ForeignKey('tasks.id')),

        sa.Column('created_at', sau.ArrowType(timezone=True), server_default=sa.text('clock_timestamp()'),
                  nullable=False, index=True),
        sa.Column('updated_at', sau.ArrowType(timezone=True), server_default=sa.text('clock_timestamp()'),
                  onupdate=sa.text('clock_timestamp()'),
                  nullable=False),

    )

    op.create_table(
        'zones',
        sa.Column('id', sau.UUIDType, server_default=sa.text("uuid_generate_v4()"), primary_key=True),
        sa.Column('name', sa.String, unique=True, nullable=False),
        sa.Column('region_id', sau.UUIDType, sa.ForeignKey('regions.id'), nullable=False),
        sa.Column('vm_cluster', sa.String, nullable=False),
        sa.Column('vm_datastore', sa.String, nullable=False),
        sa.Column('vm_folder', sa.String),
        sa.Column('core_provision_percent', sa.Integer, nullable=False),
        sa.Column('ram_provision_percent', sa.Integer, nullable=False),
        sa.Column('schedulable', sa.Boolean, nullable=False),

        sa.Column('state', sa.Enum(ZoneState), default=ZoneState.CREATING, nullable=False),
        sa.Column('current_task_id', sau.UUIDType, sa.ForeignKey('tasks.id')),

        sa.Column('created_at', sau.ArrowType(timezone=True), server_default=sa.text('clock_timestamp()'),
                  nullable=False, index=True),
        sa.Column('updated_at', sau.ArrowType(timezone=True), server_default=sa.text('clock_timestamp()'),
                  onupdate=sa.text('clock_timestamp()'),
                  nullable=False),

    )


def downgrade():
    op.drop_table('zones')
    op.drop_table('regions')
