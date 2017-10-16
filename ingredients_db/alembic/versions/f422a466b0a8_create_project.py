"""create project

Revision ID: f422a466b0a8
Revises: 458762cd0419
Create Date: 2017-09-17 09:55:16.501798

"""
import sqlalchemy as sa
import sqlalchemy_utils as sau
from alembic import op

# revision identifiers, used by Alembic.
from ingredients_db.models.project import ProjectState

revision = 'f422a466b0a8'
down_revision = '458762cd0419'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'projects',
        sa.Column('id', sau.UUIDType, server_default=sa.text("uuid_generate_v4()"), primary_key=True),
        sa.Column('name', sa.String, unique=True, nullable=False),
        sa.Column('state', sa.Enum(ProjectState), default=ProjectState.CREATED, nullable=False),

        sa.Column('created_at', sau.ArrowType(timezone=True), server_default=sa.func.now(), nullable=False, index=True),
        sa.Column('updated_at', sau.ArrowType(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(),
                  nullable=False)
    )

    op.create_table(
        'authn_tokens',
        sa.Column('id', sau.UUIDType, server_default=sa.text("uuid_generate_v4()"), primary_key=True),
        sa.Column('access_token', sa.String, nullable=False, index=True),

        sa.Column('user_id', sau.UUIDType, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('project_id', sau.UUIDType, sa.ForeignKey('projects.id', ondelete='CASCADE')),

        sa.Column('created_at', sau.ArrowType(timezone=True), server_default=sa.func.now(), nullable=False, index=True),
        sa.Column('updated_at', sau.ArrowType(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(),
                  nullable=False),
        sa.Column('expires_at', sau.ArrowType(timezone=True), nullable=False)
    )


def downgrade():
    op.drop_table('authn_token')
    op.drop_table('projects')
