"""create image

Revision ID: 52923fe51ede
Revises: f422a466b0a8
Create Date: 2017-09-17 09:55:58.239260

"""
import sqlalchemy as sa
import sqlalchemy_utils as sau
from alembic import op

from ingredients_db.models.images import ImageVisibility, ImageState

# revision identifiers, used by Alembic.

revision = '52923fe51ede'
down_revision = 'f422a466b0a8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'images',
        sa.Column('id', sau.UUIDType, sa.ForeignKey('taskable_entities.id'), primary_key=True),

        sa.Column('name', sa.String, nullable=False),
        sa.Column('file_name', sa.String, unique=True, nullable=False),
        sa.Column('locked', sa.Boolean, default=False, nullable=False),

        sa.Column('state', sa.Enum(ImageState), default=ImageState.CREATING, nullable=False),
        sa.Column('visibility', sa.Enum(ImageVisibility), default=ImageVisibility.PRIVATE, nullable=False),

        sa.Column('project_id', sau.UUIDType, sa.ForeignKey('projects.id', ondelete='RESTRICT'), nullable=False),
    )

    op.create_table(
        'image_members',
        sa.Column('image_id', sau.UUIDType, sa.ForeignKey('images.id', ondelete='CASCADE'), nullable=False,
                  primary_key=True),
        sa.Column('project_id', sau.UUIDType, sa.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False,
                  primary_key=True),

        sa.Column('created_at', sau.ArrowType(timezone=True), server_default=sa.func.now(), nullable=False, index=True),
    )


def downgrade():
    op.drop_table('image_members')
    op.drop_table('images')