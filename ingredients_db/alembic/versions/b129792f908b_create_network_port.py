"""create network port

Revision ID: b129792f908b
Revises: 9d6460001e00
Create Date: 2017-09-17 13:16:53.698284

"""
import sqlalchemy as sa
import sqlalchemy_utils as sau
from alembic import op

# revision identifiers, used by Alembic.
revision = 'b129792f908b'
down_revision = '9d6460001e00'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'network_ports',
        sa.Column('id', sau.UUIDType, server_default=sa.text("uuid_generate_v4()"), primary_key=True),

        sa.Column('network_id', sau.UUIDType, sa.ForeignKey('networks.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('project_id', sau.UUIDType, sa.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False,
                  index=True),
        sa.Column('ip_address', sau.IPAddressType),

        sa.Column('created_at', sau.ArrowType(timezone=True), server_default=sa.text('clock_timestamp()'),
                  nullable=False, index=True),
        sa.Column('updated_at', sau.ArrowType(timezone=True), server_default=sa.text('clock_timestamp()'),
                  onupdate=sa.text('clock_timestamp()'),
                  nullable=False)
    )


def downgrade():
    op.drop_table('network_ports')
