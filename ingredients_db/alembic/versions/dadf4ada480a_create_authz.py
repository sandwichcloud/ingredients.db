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
        sa.Column('description', sa.String),
        sa.Column('tags', sa.ARRAY(sa.String)),
        sa.Column('created_at', sau.ArrowType(timezone=True), server_default=sa.text('clock_timestamp()'),
                  nullable=False, index=True),
        sa.Column('updated_at', sau.ArrowType(timezone=True), server_default=sa.text('clock_timestamp()'),
                  onupdate=sa.text('clock_timestamp()'), nullable=False)
    )

    roles_table = op.create_table(
        'authz_roles',
        sa.Column('id', sau.UUIDType, server_default=sa.text("uuid_generate_v4()"), primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('project_id', sau.UUIDType, sa.ForeignKey('projects.id', ondelete='CASCADE')),
        sa.Column('description', sa.String),
        sa.Column('created_at', sau.ArrowType(timezone=True), server_default=sa.text('clock_timestamp()'),
                  nullable=False, index=True),
        sa.Column('updated_at', sau.ArrowType(timezone=True), server_default=sa.text('clock_timestamp()'),
                  onupdate=sa.text('clock_timestamp()'), nullable=False)
    )
    op.create_unique_constraint('uq_name_project_id', 'authz_roles', ['name', 'project_id'])

    role_policies_table = op.create_table(
        'authz_role_policies',
        sa.Column('id', sau.UUIDType, server_default=sa.text("uuid_generate_v4()"), primary_key=True),
        sa.Column('role_id', sau.UUIDType, sa.ForeignKey('authz_roles.id', ondelete='CASCADE'), index=True,
                  nullable=False),
        sa.Column('policy_id', sau.UUIDType, sa.ForeignKey('authz_policies.id', ondelete='CASCADE'), index=True,
                  nullable=False),
        sa.Column('created_at', sau.ArrowType(timezone=True), server_default=sa.text('clock_timestamp()'),
                  nullable=False, index=True),
        sa.Column('updated_at', sau.ArrowType(timezone=True), server_default=sa.text('clock_timestamp()'),
                  onupdate=sa.text('clock_timestamp()'), nullable=False)
    )

    op.create_table(
        'authn_service_accounts',
        sa.Column('id', sau.UUIDType, server_default=sa.text("uuid_generate_v4()"), primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('project_id', sau.UUIDType, sa.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False),
        sa.Column('role_id', sau.UUIDType, sa.ForeignKey('authz_roles.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('created_at', sau.ArrowType(timezone=True), server_default=sa.text('clock_timestamp()'),
                  nullable=False, index=True),
        sa.Column('updated_at', sau.ArrowType(timezone=True), server_default=sa.text('clock_timestamp()'),
                  onupdate=sa.text('clock_timestamp()'), nullable=False)
    )

    # TODO: add project_members
    op.create_table(
        'project_members',
        sa.Column('id', sau.UUIDType, server_default=sa.text("uuid_generate_v4()"), primary_key=True),
        sa.Column('user_id', sau.UUIDType, sa.ForeignKey('authn_users.id', ondelete='CASCADE'), nullable=False,
                  index=True),
        sa.Column('project_id', sau.UUIDType, sa.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False,
                  index=True),
        sa.Column('role_id', sau.UUIDType, sa.ForeignKey('authz_roles.id', ondelete='RESTRICT'), nullable=False,
                  index=True),
        sa.Column('created_at', sau.ArrowType(timezone=True), server_default=sa.text('clock_timestamp()'),
                  nullable=False, index=True),
        sa.Column('updated_at', sau.ArrowType(timezone=True), server_default=sa.text('clock_timestamp()'),
                  onupdate=sa.text('clock_timestamp()'), nullable=False)
    )

    op.bulk_insert(
        roles_table,
        [
            {
                "name": "admin",
                "description": "Administrator Role"
            },
            {
                "name": "viewer",
                "description": "Viewer role; has the ability to view non-project level objects"
            }
        ]
    )

    # Policy Tags:
    # viewer - policies the viewer role should have
    # project_member - policies the default project member role should have
    # service_account - policies the default project service account role should have
    op.bulk_insert(
        policies_table,
        [
            # Policies
            {
                "name": "policies:create",
                "description": "Ability to create a policy",
            },
            {
                "name": "policies:get",
                "description": "Ability to get a policy",
                "tags": [
                    "viewer"
                ]

            },
            {
                "name": "policies:update",
                "description": "Ability to update a policy"
            },
            {
                "name": "policies:list",
                "description": "Ability to list policies",
                "tags": [
                    "viewer"
                ]
            },
            {
                "name": "policies:delete",
                "description": "Ability to delete a policy"
            },

            # Roles
            {
                "name": "roles:create:global",
                "description": "Ability to create a global role"
            },
            {
                "name": "roles:delete:global",
                "description": "Ability to delete a global role"
            },
            {
                "name": "roles:create:project",
                "description": "Ability to create a project role",
                "tags": [
                    "project_member"
                ]
            },
            {
                "name": "roles:delete:project",
                "description": "Ability to delete a project role",
                "tags": [
                    "project_member"
                ]
            },
            {
                "name": "roles:get",
                "description": "Ability to get a role",
                "tags": [
                    "viewer"
                ]
            },
            {
                "name": "roles:list",
                "description": "Ability to list roles",
                "tags": [
                    "viewer"
                ]
            },

            # Regions
            {
                "name": "regions:create",
                "description": "Ability to create a region"
            },
            {
                "name": "regions:get",
                "description": "Ability to get a region",
                "tags": [
                    "viewer"
                ]
            },
            {
                "name": "regions:list",
                "description": "Ability to list regions",
                "tags": [
                    "viewer"
                ]
            },
            {
                "name": "regions:delete",
                "description": "Ability to delete a region"
            },
            {
                "name": "regions:action:schedule",
                "description": "Ability to change the schedule mode of the region"
            },

            # Zones
            {
                "name": "zones:create",
                "description": "Ability to create a zone"
            },
            {
                "name": "zones:get",
                "description": "Ability to get a zone",
                "tags": [
                    "viewer"
                ]
            },
            {
                "name": "zones:list",
                "description": "Ability to list zones",
                "tags": [
                    "viewer"
                ]
            },
            {
                "name": "zones:delete",
                "description": "Ability to delete a zone"
            },
            {
                "name": "zones:action:schedule",
                "description": "Ability to change the schedule mode of the zone"
            },

            # Projects
            {
                "name": "projects:create",
                "description": "Ability to create a project"
            },
            {
                "name": "projects:get",
                "description": "Ability to get a project",
                "tags": [
                    "viewer"
                ]
            },
            {
                "name": "projects:list",
                "description": "Ability to list projects",
                "tags": [
                    "viewer"
                ]
            },
            {
                "name": "projects:delete",
                "description": "Ability to delete a project"
            },
            # TODO: add policies for project:members

            # Tasks

            # Images
            {
                "name": "images:create",
                "description": "Ability to create an image",
                "tags": [
                    "project_member"
                ]
            },
            {
                "name": "images:create:public",
                "description": "Ability to create a public image"
            },
            {
                "name": "images:get",
                "description": "Ability to get an image",
                "tags": [
                    "project_member",
                    "service_account"
                ]
            },
            {
                "name": "images:list",
                "description": "Ability to list images",
                "tags": [
                    "project_member",
                    "service_account"
                ]
            },
            {
                "name": "images:delete",
                "description": "Ability to delete an image",
                "tags": [
                    "project_member"
                ]
            },
            {
                "name": "images:action:lock",
                "description": "Ability to lock an image",
                "tags": [
                    "project_member"
                ]
            },
            {
                "name": "images:action:unlock",
                "description": "Ability to unlock an image",
                "tags": [
                    "project_member"
                ]
            },

            # Instances
            {
                "name": "instances:create",
                "description": "Ability to create an instance",
                "tags": [
                    "project_member"
                ]
            },
            {
                "name": "instances:get",
                "description": "Ability to get an instance",
                "tags": [
                    "project_member",
                    "service_account"
                ]
            },
            {
                "name": "instances:list",
                "description": "Ability to list instances",
                "tags": [
                    "project_member",
                    "service_account"
                ]
            },
            {
                "name": "instances:delete",
                "description": "Ability to delete an instance",
                "tags": [
                    "project_member"
                ]
            },
            {
                "name": "instances:action:stop",
                "description": "Ability to stop an instance",
                "tags": [
                    "project_member"
                ]
            },
            {
                "name": "instances:action:start",
                "description": "Ability to start an instance",
                "tags": [
                    "project_member"
                ]
            },
            {
                "name": "instances:action:restart",
                "description": "Ability to restart an instance",
                "tags": [
                    "project_member"
                ]
            },
            {
                "name": "instances:action:image",
                "description": "Ability to create an image from an instance",
                "tags": [
                    "project_member"
                ]
            },
            {
                "name": "instances:action:image:public",
                "description": "Ability to create a public image from an instance"
            },
            {
                "name": "instances:action:reset_state",
                "description": "Ability to reset the state of an instance to error",
                "tags": [
                    "project_member"
                ]
            },
            {
                "name": "instances:action:reset_state:active",
                "description": "Ability to reset the state of an instance to active",
                "tags": [
                    "project_member"
                ]
            },

            # Networks
            {
                "name": "networks:create",
                "description": "Ability to create a network"
            },
            {
                "name": "networks:get",
                "description": "Ability to get a network",
                "tags": [
                    "viewer"
                ]
            },
            {
                "name": "networks:list",
                "description": "Ability to list networks",
                "tags": [
                    "viewer"
                ]
            },
            {
                "name": "networks:delete",
                "description": "Ability to delete a network"
            },

            # Service Accounts
            {
                "name": "service_accounts:create",
                "description": "Ability to create a service account",
                "tags": [
                    "project_member"
                ]
            },
            {
                "name": "service_accounts:get",
                "description": "Ability to get a service account",
                "tags": [
                    "project_member",
                    "service_account"
                ]
            },
            {
                "name": "service_accounts:list",
                "description": "Ability to list service accounts",
                "tags": [
                    "project_member",
                    "service_account"
                ]
            },
            {
                "name": "service_accounts:delete",
                "description": "Ability to delete a service account",
                "tags": [
                    "project_member"
                ]
            },

            # BuiltIn Users
            {
                "name": "builtin:users:create",
                "description": "Ability to create users",
            },
            {
                "name": "builtin:users:get",
                "description": "Ability to get a user",
                "tags": [
                    "viewer"
                ]
            },
            {
                "name": "builtin:users:list",
                "description": "Ability to list users",
                "tags": [
                    "viewer"
                ]
            },
            {
                "name": "builtin:users:delete",
                "description": "Ability to delete a user"
            },
            {
                "name": "builtin:users:password",
                "description": "Ability to change a user's password"
            },
            {
                "name": "builtin:users:role:add",
                "description": "Ability to add a role to a user"
            },
            {
                "name": "builtin:users:role:remove",
                "description": "Ability to remove a user from a role"
            },

            # Keypairs
            {
                "name": "keypairs:create",
                "description": "Ability to create a keypair",
                "tags": [
                    "project_member"
                ]
            },
            {
                "name": "keypairs:get",
                "description": "Ability to get a keypair",
                "tags": [
                    "project_member",
                    "service_account"
                ]
            },
            {
                "name": "keypairs:list",
                "description": "Ability to list keypairs",
                "tags": [
                    "project_member",
                    "service_account"
                ]
            },
            {
                "name": "keypairs:delete",
                "description": "Ability to delete a keypair",
                "tags": [
                    "project_member"
                ]
            },

            # Network Ports
            {
                "name": "network_ports:get",
                "description": "Ability to get a network port",
                "tags": [
                    "project_member",
                    "service_account"
                ]
            },
            {
                "name": "network_ports:list",
                "description": "Ability to list  network ports",
                "tags": [
                    "project_member",
                    "service_account"
                ]
            },
            {
                "name": "network_ports:delete",
                "description": "Ability to delete a network port",
                "tags": [
                    "project_member"
                ]
            }

        ],
        multiinsert=False  # Needed so the list insert works correctly
    )

    connection = op.get_bind()
    admin_role = connection.execute(roles_table.select().where(roles_table.c.name == "admin")).fetchone()
    viewer_role = connection.execute(roles_table.select().where(roles_table.c.name == "viewer")).fetchone()
    for policy in connection.execute(policies_table.select()):
        connection.execute(
            role_policies_table.insert().values(
                role_id=admin_role.id,
                policy_id=policy.id
            )
        )
        if policy.tags is not None:
            if 'viewer' in policy.tags:
                connection.execute(
                    role_policies_table.insert().values(
                        role_id=viewer_role.id,
                        policy_id=policy.id
                    )
                )


def downgrade():
    op.drop_table('authn_service_accounts')
    op.drop_table('authz_role_policies')
    op.drop_table('project_members')
    op.drop_table('authz_roles')
    op.drop_table('authz_policies')
