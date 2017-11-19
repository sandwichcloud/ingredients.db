"""create image

Revision ID: 52923fe51ede
Revises: dadf4ada480a
Create Date: 2017-09-17 09:55:58.239260

"""
import sqlalchemy as sa
import sqlalchemy_utils as sau
from alembic import op

from ingredients_db.models.images import ImageVisibility, ImageState

# revision identifiers, used by Alembic.

revision = '52923fe51ede'
down_revision = 'dadf4ada480a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'images',
        sa.Column('id', sau.UUIDType, server_default=sa.text("uuid_generate_v4()"), primary_key=True),

        sa.Column('name', sa.String, nullable=False),
        sa.Column('file_name', sa.String, unique=True, nullable=False),
        sa.Column('locked', sa.Boolean, default=False, nullable=False),

        sa.Column('state', sa.Enum(ImageState), default=ImageState.CREATING, nullable=False),
        sa.Column('visibility', sa.Enum(ImageVisibility), default=ImageVisibility.PRIVATE, nullable=False),

        sa.Column('project_id', sau.UUIDType, sa.ForeignKey('projects.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('region_id', sau.UUIDType, sa.ForeignKey('regions.id'), nullable=False),

        sa.Column('current_task_id', sau.UUIDType, sa.ForeignKey('tasks.id')),
        sa.Column('created_at', sau.ArrowType(timezone=True), server_default=sa.text('clock_timestamp()'),
                  nullable=False, index=True),
        sa.Column('updated_at', sau.ArrowType(timezone=True), server_default=sa.text('clock_timestamp()'),
                  onupdate=sa.text('clock_timestamp()'),
                  nullable=False),
    )

    op.create_table(
        'image_members',
        sa.Column('image_id', sau.UUIDType, sa.ForeignKey('images.id', ondelete='CASCADE'), nullable=False,
                  primary_key=True),
        sa.Column('project_id', sau.UUIDType, sa.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False,
                  primary_key=True),

        sa.Column('created_at', sau.ArrowType(timezone=True), server_default=sa.text('clock_timestamp()'),
                  nullable=False, index=True),
    )


def downgrade():
    op.drop_table('image_members')
    op.drop_table('images')
