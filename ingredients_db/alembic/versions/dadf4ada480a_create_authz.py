"""create authz

Revision ID: dadf4ada480a
Revises: f422a466b0a8
Create Date: 2017-10-16 18:03:47.841570

"""
import sqlalchemy as sa
import sqlalchemy_utils as sau
from alembic import op

# revision identifiers, used by Alembic.
revision = 'dadf4ada480a'
down_revision = 'f422a466b0a8'
branch_labels = None
depends_on = None


def upgrade():
    policies_table = op.create_table(
        'authz_policies',
        sa.Column('id', sau.UUIDType, server_default=sa.text("uuid_generate_v4()"), primary_key=True),
        sa.Column('name', sa.String, nullable=False, unique=True),
        sa.Column('rule', sa.String, nullable=False),
        sa.Column('description', sa.String),
        sa.Column('created_at', sau.ArrowType(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sau.ArrowType(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(),
                  nullable=False)
    )

    # rules_table = op.create_table(
    #     'authz_rules',
    #     sa.Column('id', sau.UUIDType, server_default=sa.text("uuid_generate_v4()"), primary_key=True),
    #     sa.Column('name', sa.String, nullable=False, unique=True),
    #     sa.Column('value', sa.String, nullable=False),
    #     sa.Column('description', sa.String),
    #     sa.Column('created_at', sau.ArrowType(timezone=True), server_default=sa.func.now(), nullable=False),
    #     sa.Column('updated_at', sau.ArrowType(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(),
    #               nullable=False)
    # )

    roles_table = op.create_table(
        'authz_roles',
        sa.Column('id', sau.UUIDType, server_default=sa.text("uuid_generate_v4()"), primary_key=True),
        sa.Column('name', sa.String, nullable=False, unique=True),
        sa.Column('description', sa.String),
        sa.Column('created_at', sau.ArrowType(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sau.ArrowType(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(),
                  nullable=False)
    )

    op.create_table(
        'authn_tokens',
        sa.Column('id', sau.UUIDType, server_default=sa.text("uuid_generate_v4()"), primary_key=True),
        sa.Column('access_token', sa.String, nullable=False, index=True),

        sa.Column('user_id', sau.UUIDType, sa.ForeignKey('authn_users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('project_id', sau.UUIDType, sa.ForeignKey('projects.id', ondelete='CASCADE')),

        sa.Column('created_at', sau.ArrowType(timezone=True), server_default=sa.func.now(), nullable=False, index=True),
        sa.Column('updated_at', sau.ArrowType(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(),
                  nullable=False),
        sa.Column('expires_at', sau.ArrowType(timezone=True), nullable=False)
    )

    op.create_table(
        'authn_token_roles',
        sa.Column('id', sau.UUIDType, server_default=sa.text("uuid_generate_v4()"), primary_key=True),

        sa.Column('token_id', sau.UUIDType, sa.ForeignKey('authn_tokens.id', ondelete='CASCADE'), nullable=False),
        sa.Column('role_id', sau.UUIDType, sa.ForeignKey('authz_roles.id', ondelete='CASCADE'), nullable=False),

        sa.Column('updated_at', sau.ArrowType(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(),
                  nullable=False),
    )

    # TODO: populate default roles

    op.bulk_insert(
        roles_table,
        [
            {"name": "admin", "description": "Administrator Role for Sandwich Cloud"}
        ]
    )

    op.bulk_insert(
        policies_table,
        [
            # Rules
            {"name": "is_admin", "rule": "role:admin", "description": "Is the user in the admin role"},
            {"name": "admin_or_member", "rule": "rule:is_admin or project_id:%(project_id)s",
             "description": "Is the user in the admin role"},

            # Policies

            # Roles

            # Tokens

            # Tasks

            # Projects
            {"name": "projects:create", "rule": "rule:is_admin", "description": "Ability to create projects"},
            {"name": "projects:get", "rule": "", "description": "Ability to get a project"},
            {"name": "projects:list", "rule": "", "description": "Ability to list projects"},
            {"name": "projects:delete", "rule": "rule:is_admin", "description": "Ability to delete projects"},

            # Networks

            # Images
            {"name": "images:create", "rule": "rule:admin_or_member", "description": "Ability to create images"},

            # Instances
        ]
    )

    # TODO: populate default policies
    #


def downgrade():
    op.drop_table('authn_token_roles')
    op.drop_table('authn_tokens')
    op.drop_table('authz_roles')
    # op.drop_table('authz_rules')
    op.drop_table('authz_policies')
