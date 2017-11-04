"""create network

Revision ID: 9d6460001e00
Revises: 52923fe51ede
Create Date: 2017-09-17 10:17:05.262655

"""
import sqlalchemy as sa
import sqlalchemy_utils as sau
from alembic import op

# revision identifiers, used by Alembic.
from ingredients_db.models.network import NetworkState
from ingredients_db.types import IPv4Network

revision = '9d6460001e00'
down_revision = '52923fe51ede'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'networks',
        sa.Column('id', sau.UUIDType, server_default=sa.text("uuid_generate_v4()"), primary_key=True),
        sa.Column('name', sa.String, unique=True, nullable=False),
        sa.Column('current_task_id', sau.UUIDType, sa.ForeignKey('tasks.id')),

        sa.Column('port_group', sa.String, unique=True, nullable=False),
        sa.Column('gateway', sau.IPAddressType, nullable=False),
        sa.Column('dns_servers', sa.ARRAY(sau.IPAddressType), nullable=False),

        sa.Column('state', sa.Enum(NetworkState), default=NetworkState.CREATING, nullable=False),

        sa.Column('cidr', IPv4Network, nullable=False),
        sa.Column('pool_start', sau.IPAddressType, nullable=False),
        sa.Column('pool_end', sau.IPAddressType, nullable=False),
        sa.Column('created_at', sau.ArrowType(timezone=True), server_default=sa.text('clock_timestamp()'),
                  nullable=False, index=True),
        sa.Column('updated_at', sau.ArrowType(timezone=True), server_default=sa.text('clock_timestamp()'),
                  onupdate=sa.text('clock_timestamp()'),
                  nullable=False),

    )


def downgrade():
    op.drop_table('networks')
