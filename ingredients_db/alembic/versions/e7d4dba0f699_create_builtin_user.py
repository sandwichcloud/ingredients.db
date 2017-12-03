"""create builtin user

Revision ID: e7d4dba0f699
Revises: ba0652dfa1be
Create Date: 2017-12-02 18:13:36.109525

"""
import sqlalchemy as sa
import sqlalchemy_utils as sau
from alembic import op
from sqlalchemy.dialects.postgresql import ARRAY

# revision identifiers, used by Alembic.
revision = 'e7d4dba0f699'
down_revision = 'ba0652dfa1be'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'builtin_users',
        sa.Column('id', sau.UUIDType, server_default=sa.text("uuid_generate_v4()"), primary_key=True),
        sa.Column('username', sa.String, nullable=False, unique=True),
        sa.Column('password', sau.PasswordType(schemes=['bcrypt']), nullable=False),
        sa.Column('roles', ARRAY(sa.String), default=list),
        sa.Column('created_at', sau.ArrowType(timezone=True), server_default=sa.text('clock_timestamp()'),
                  nullable=False, index=True),
        sa.Column('updated_at', sau.ArrowType(timezone=True), server_default=sa.text('clock_timestamp()'),
                  onupdate=sa.text('clock_timestamp()'),
                  nullable=False)
    )


def downgrade():
    op.drop_table('builtin_users')
