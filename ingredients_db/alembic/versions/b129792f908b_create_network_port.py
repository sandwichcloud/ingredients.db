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
        sa.Column('ip_address', sau.IPAddressType),

        sa.Column('created_at', sau.ArrowType(timezone=True), server_default=sa.func.now(), nullable=False, index=True),
        sa.Column('updated_at', sau.ArrowType(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(),
                  nullable=False)
    )

    op.create_table(
        'networkable_entities',
        sa.Column('id', sau.UUIDType, sa.ForeignKey('taskable_entities.id'), primary_key=True),
        sa.Column('network_port_id', sau.UUIDType, sa.ForeignKey('network_ports.id', ondelete='SET NULL')),
    )


def downgrade():
    op.drop_table('networkable_entities')
    op.drop_table('network_ports')
