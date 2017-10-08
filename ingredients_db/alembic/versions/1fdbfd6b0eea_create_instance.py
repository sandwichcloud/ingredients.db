"""create instance

Revision ID: 1fdbfd6b0eea
Revises: b129792f908b
Create Date: 2017-09-17 13:17:52.136597

"""
import sqlalchemy as sa
import sqlalchemy_utils as sau
from alembic import op
# revision identifiers, used by Alembic.
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import HSTORE

from ingredients_db.models.instance import InstanceState

revision = '1fdbfd6b0eea'
down_revision = 'b129792f908b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'instances',
        sa.Column('id', sau.UUIDType, ForeignKey('networkable_entities.id'), primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('tags', HSTORE),
        sa.Column('state', sa.Enum(InstanceState), default=InstanceState.BUILDING, nullable=False),

        sa.Column('project_id', sau.UUIDType, sa.ForeignKey('projects.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('image_id', sau.UUIDType, sa.ForeignKey('images.id', ondelete='SET NULL'))

    )


def downgrade():
    op.drop_table('instances')