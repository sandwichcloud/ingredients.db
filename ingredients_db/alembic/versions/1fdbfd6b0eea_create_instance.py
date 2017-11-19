"""create instance

Revision ID: 1fdbfd6b0eea
Revises: b129792f908b
Create Date: 2017-09-17 13:17:52.136597

"""
import sqlalchemy as sa
import sqlalchemy_utils as sau
from alembic import op
# revision identifiers, used by Alembic.
from sqlalchemy.dialects.postgresql import HSTORE

from ingredients_db.models.instance import InstanceState

revision = '1fdbfd6b0eea'
down_revision = 'b129792f908b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'instances',
        sa.Column('id', sau.UUIDType, server_default=sa.text("uuid_generate_v4()"), primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('tags', HSTORE),
        sa.Column('state', sa.Enum(InstanceState), default=InstanceState.BUILDING, nullable=False),
        sa.Column('network_port_id', sau.UUIDType, sa.ForeignKey('network_ports.id', ondelete='RESTRICT')),
        sa.Column('region_id', sau.UUIDType, sa.ForeignKey('regions.id'), nullable=False),
        sa.Column('zone_id', sau.UUIDType, sa.ForeignKey('zones.id')),

        sa.Column('project_id', sau.UUIDType, sa.ForeignKey('projects.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('current_task_id', sau.UUIDType, sa.ForeignKey('tasks.id')),
        sa.Column('image_id', sau.UUIDType, sa.ForeignKey('images.id', ondelete='SET NULL')),
        sa.Column('created_at', sau.ArrowType(timezone=True), server_default=sa.text('clock_timestamp()'),
                  nullable=False, index=True),
        sa.Column('updated_at', sau.ArrowType(timezone=True), server_default=sa.text('clock_timestamp()'),
                  onupdate=sa.text('clock_timestamp()'),
                  nullable=False),

    )


def downgrade():
    op.drop_table('instances')
