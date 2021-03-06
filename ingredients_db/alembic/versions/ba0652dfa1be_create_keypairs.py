"""create keypairs

Revision ID: ba0652dfa1be
Revises: 1fdbfd6b0eea
Create Date: 2017-10-03 08:41:39.240401

"""
import sqlalchemy as sa
import sqlalchemy_utils as sau
from alembic import op

# revision identifiers, used by Alembic.
revision = 'ba0652dfa1be'
down_revision = '1fdbfd6b0eea'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'keypairs',
        sa.Column('id', sau.UUIDType, server_default=sa.text("uuid_generate_v4()"), primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('public_key', sa.Text, nullable=False),

        sa.Column('project_id', sau.UUIDType, sa.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False),

        sa.Column('created_at', sau.ArrowType(timezone=True), server_default=sa.text('clock_timestamp()'),
                  nullable=False, index=True),
        sa.Column('updated_at', sau.ArrowType(timezone=True), server_default=sa.text('clock_timestamp()'),
                  onupdate=sa.text('clock_timestamp()'),
                  nullable=False)
    )

    op.create_table(
        'instance_keypairs',
        sa.Column('id', sau.UUIDType, server_default=sa.text("uuid_generate_v4()"), primary_key=True),

        sa.Column('keypair_id', sau.UUIDType, sa.ForeignKey('keypairs.id', ondelete='CASCADE')),
        sa.Column('instance_id', sau.UUIDType, sa.ForeignKey('instances.id', ondelete='CASCADE')),

        sa.Column('created_at', sau.ArrowType(timezone=True), server_default=sa.text('clock_timestamp()'),
                  nullable=False, index=True),
        sa.Column('updated_at', sau.ArrowType(timezone=True), server_default=sa.text('clock_timestamp()'),
                  onupdate=sa.text('clock_timestamp()'),
                  nullable=False)
    )


def downgrade():
    op.drop_table('instance_keypairs')
    op.drop_table('keypairs')
