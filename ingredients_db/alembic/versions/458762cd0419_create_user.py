"""create user

Revision ID: 458762cd0419
Revises: 3ce1572cbc6b
Create Date: 2017-09-16 09:24:55.054833

"""
import sqlalchemy as sa
import sqlalchemy_utils as sau
from alembic import op

# revision identifiers, used by Alembic.
revision = '458762cd0419'
down_revision = '3ce1572cbc6b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sau.UUIDType, server_default=sa.text("uuid_generate_v4()"), primary_key=True),
        sa.Column('username', sa.String, unique=True, nullable=False),
        sa.Column('created_at', sau.ArrowType(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sau.ArrowType(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(),
                  nullable=False)
    )


def downgrade():
    op.drop_table('users')
