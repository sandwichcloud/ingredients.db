"""create authz

Revision ID: dadf4ada480a
Revises: ba0652dfa1be
Create Date: 2017-10-16 18:03:47.841570

"""
import sqlalchemy as sa
import sqlalchemy_utils as sau
from alembic import op

# revision identifiers, used by Alembic.
revision = 'dadf4ada480a'
down_revision = 'ba0652dfa1be'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'authz_policies',
        sa.Column('id', sau.UUIDType, server_default=sa.text("uuid_generate_v4()"), primary_key=True),
        sa.Column('name', sa.String, nullable=False, unique=True),
        sa.Column('value', sa.String, nullable=False),
        sa.Column('description', sa.String),
        sa.Column('created_at', sau.ArrowType(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sau.ArrowType(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(),
                  nullable=False)
    )

    op.create_table(
        'authz_rules',
        sa.Column('id', sau.UUIDType, server_default=sa.text("uuid_generate_v4()"), primary_key=True),
        sa.Column('name', sa.String, nullable=False, unique=True),
        sa.Column('value', sa.String, nullable=False),
        sa.Column('description', sa.String),
        sa.Column('created_at', sau.ArrowType(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sau.ArrowType(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(),
                  nullable=False)
    )

    op.create_table(
        'authz_roles',
        sa.Column('id', sau.UUIDType, server_default=sa.text("uuid_generate_v4()"), primary_key=True),
        sa.Column('name', sa.String, nullable=False, unique=True),
        sa.Column('created_at', sau.ArrowType(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sau.ArrowType(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(),
                  nullable=False)
    )


def downgrade():
    op.drop_table('authz_roles')
    op.drop_table('authz_rules')
    op.drop_table('authz_policies')
