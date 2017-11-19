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
        sa.Column('created_at', sau.ArrowType(timezone=True), server_default=sa.text('clock_timestamp()'),
                  nullable=False),
        sa.Column('updated_at', sau.ArrowType(timezone=True), server_default=sa.text('clock_timestamp()'),
                  onupdate=sa.text('clock_timestamp()'),
                  nullable=False)
    )

    roles_table = op.create_table(
        'authz_roles',
        sa.Column('id', sau.UUIDType, server_default=sa.text("uuid_generate_v4()"), primary_key=True),
        sa.Column('name', sa.String, nullable=False, unique=True),
        sa.Column('description', sa.String),
        sa.Column('created_at', sau.ArrowType(timezone=True), server_default=sa.text('clock_timestamp()'),
                  nullable=False),
        sa.Column('updated_at', sau.ArrowType(timezone=True), server_default=sa.text('clock_timestamp()'),
                  onupdate=sa.text('clock_timestamp()'),
                  nullable=False)
    )

    op.create_table(
        'authn_tokens',
        sa.Column('id', sau.UUIDType, server_default=sa.text("uuid_generate_v4()"), primary_key=True),
        sa.Column('access_token', sa.String, nullable=False, index=True),

        sa.Column('user_id', sau.UUIDType, sa.ForeignKey('authn_users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('project_id', sau.UUIDType, sa.ForeignKey('projects.id', ondelete='CASCADE')),

        sa.Column('created_at', sau.ArrowType(timezone=True), server_default=sa.text('clock_timestamp()'),
                  nullable=False, index=True),
        sa.Column('updated_at', sau.ArrowType(timezone=True), server_default=sa.text('clock_timestamp()'),
                  onupdate=sa.text('clock_timestamp()'),
                  nullable=False),
        sa.Column('expires_at', sau.ArrowType(timezone=True), nullable=False)
    )

    op.create_table(
        'authn_token_roles',
        sa.Column('id', sau.UUIDType, server_default=sa.text("uuid_generate_v4()"), primary_key=True),

        sa.Column('token_id', sau.UUIDType, sa.ForeignKey('authn_tokens.id', ondelete='CASCADE'), nullable=False),
        sa.Column('role_id', sau.UUIDType, sa.ForeignKey('authz_roles.id', ondelete='CASCADE'), nullable=False),

        sa.Column('created_at', sau.ArrowType(timezone=True), server_default=sa.text('clock_timestamp()'),
                  nullable=False, index=True),
        sa.Column('updated_at', sau.ArrowType(timezone=True), server_default=sa.text('clock_timestamp()'),
                  onupdate=sa.text('clock_timestamp()'),
                  nullable=False),
    )

    op.bulk_insert(
        roles_table,
        [
            {"name": "admin", "description": "Administrator Role"}
        ]
    )

    op.bulk_insert(
        policies_table,
        [
            # Rules
            {"name": "is_admin", "rule": "role:admin", "description": "Is the user in the admin role"},
            {"name": "admin_or_member", "rule": "rule:is_admin or project_id:%(project_id)s",
             "description": "Is the user in the admin role or a member of the project of the requested object"},
            {"name": "admin_or_self", "rule": "rule:is_admin or user_id:%(user_id)s",
             "description": "Is the user in the admin role or the requested object matches the user id"},

            # Policies
            # Use role:admin so we don't get locked out if is_admin is changed/deleted
            # If the admin role gets deleted... well don't be stupid :p
            {"name": "policies:create", "rule": "role:admin", "description": "Ability to create a policy"},
            {"name": "policies:get", "rule": "role:admin", "description": "Ability to get a policy"},
            {"name": "policies:update", "rule": "role:admin", "description": "Ability to update a policy"},
            {"name": "policies:list", "rule": "role:admin", "description": "Ability to list policies"},
            {"name": "policies:delete", "rule": "role:admin", "description": "Ability to delete a policy"},

            # Roles
            # Use role:admin so we don't get locked out if is_admin is changed/deleted
            # If the admin role gets deleted... well don't be stupid :p
            {"name": "roles:create", "rule": "role:admin", "description": "Ability to create a role"},
            {"name": "roles:get", "rule": "role:admin", "description": "Ability to get a role"},
            {"name": "roles:list", "rule": "role:admin", "description": "Ability to list roles"},
            {"name": "roles:delete", "rule": "role:admin", "description": "Ability to delete a role"},

            # Regions
            {"name": "regions:create", "rule": "role:admin", "description": "Ability to create a region"},
            {"name": "regions:get", "rule": "", "description": "Ability to get a region"},
            {"name": "regions:list", "rule": "", "description": "Ability to list regions"},
            {"name": "regions:delete", "rule": "role:admin", "description": "Ability to delete a region"},
            {"name": "regions:action:schedule", "rule": "role:admin",
             "description": "Ability to change the schedule mode of the region"},

            # Zones
            {"name": "zones:create", "rule": "role:admin", "description": "Ability to create a zone"},
            {"name": "zones:get", "rule": "", "description": "Ability to get a zone"},
            {"name": "zones:list", "rule": "", "description": "Ability to list zones"},
            {"name": "zones:delete", "rule": "role:admin", "description": "Ability to delete a zone"},
            {"name": "zones:action:schedule", "rule": "role:admin",
             "description": "Ability to change the schedule mode of the zone"},

            # Tokens
            {"name": "tokens:get", "rule": "rule:admin_or_self", "description": "Ability to get a token"},

            # Projects
            {"name": "projects:create", "rule": "rule:is_admin", "description": "Ability to create a project"},
            {"name": "projects:get", "rule": "", "description": "Ability to get a project"},
            {"name": "projects:list", "rule": "", "description": "Ability to list projects"},
            {"name": "projects:delete", "rule": "rule:is_admin", "description": "Ability to delete a project"},

            # Tasks

            # Images
            {"name": "images:create", "rule": "rule:admin_or_member", "description": "Ability to create an image"},
            {"name": "images:create:public", "rule": "rule:is_admin",
             "description": "Ability to create a public image"},
            {"name": "images:get", "rule": "rule:admin_or_member", "description": "Ability to get an image"},
            {"name": "images:list", "rule": "rule:admin_or_member", "description": "Ability to list images"},
            {"name": "images:delete", "rule": "rule:admin_or_member", "description": "Ability to delete an image"},
            {"name": "images:action:lock", "rule": "rule:admin_or_member", "description": "Ability to lock an image"},
            {"name": "images:action:unlock", "rule": "rule:admin_or_member",
             "description": "Ability to unlock an image"},

            # Instances
            {"name": "instances:create", "rule": "rule:admin_or_member",
             "description": "Ability to create an instance"},
            {"name": "instances:get", "rule": "rule:admin_or_member", "description": "Ability to get an instance"},
            {"name": "instances:list", "rule": "rule:admin_or_member", "description": "Ability to list instances"},
            {"name": "instances:delete", "rule": "rule:admin_or_member",
             "description": "Ability to delete an instance"},
            {"name": "instances:action:stop", "rule": "rule:admin_or_member",
             "description": "Ability to stop an instance"},
            {"name": "instances:action:start", "rule": "rule:admin_or_member",
             "description": "Ability to start an instance"},
            {"name": "instances:action:restart", "rule": "rule:admin_or_member",
             "description": "Ability to restart an instance"},
            {"name": "instances:action:image", "rule": "rule:admin_or_member",
             "description": "Ability to create an image from an instance"},
            {"name": "instances:action:image:public", "rule": "rule:is_admin",
             "description": "Ability to create a public image from an instance"},
            {"name": "instances:action:reset_state", "rule": "rule:admin_or_member",
             "description": "Ability to reset the state of an instance to error"},
            {"name": "instances:action:reset_state:active", "rule": "rule:is_admin",
             "description": "Ability to reset the state of an instance to active"},

            # Networks
            {"name": "networks:create", "rule": "rule:is_admin", "description": "Ability to create a network"},
            {"name": "networks:get", "rule": "", "description": "Ability to get a network"},
            {"name": "networks:list", "rule": "", "description": "Ability to list networks"},
            {"name": "networks:delete", "rule": "rule:is_admin", "description": "Ability to delete a network"},

        ]
    )


def downgrade():
    op.drop_table('authn_token_roles')
    op.drop_table('authn_tokens')
    op.drop_table('authz_roles')
    op.drop_table('authz_policies')
