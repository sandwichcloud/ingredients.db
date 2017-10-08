"""create tasks

Revision ID: 3ce1572cbc6b
Revises: 1fdbfd6b0eea
Create Date: 2017-09-24 12:13:14.977009

"""
import sqlalchemy as sa
import sqlalchemy_utils as sau
from alembic import op

# revision identifiers, used by Alembic.
from ingredients_db.models.task import TaskState

revision = '3ce1572cbc6b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'tasks',
        sa.Column('id', sau.UUIDType, server_default=sa.text("uuid_generate_v4()"), primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('state', sa.Enum(TaskState), default=TaskState.PENDING, nullable=False),
        sa.Column('error_message', sa.Text),

        sa.Column('created_at', sau.ArrowType(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sau.ArrowType(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(),
                  nullable=False),
        sa.Column('stopped_at', sau.ArrowType(timezone=True)),
    )
    op.create_table(
        'taskable_entities',
        sa.Column('id', sau.UUIDType, server_default=sa.text("uuid_generate_v4()"), primary_key=True),
        sa.Column('type', sa.String, nullable=False),

        sa.Column('current_task_id', sau.UUIDType, sa.ForeignKey('tasks.id')),

        sa.Column('created_at', sau.ArrowType(timezone=True), server_default=sa.func.now(), nullable=False, index=True),
        sa.Column('updated_at', sau.ArrowType(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(),
                  nullable=False)
    )


def downgrade():
    op.drop_table('taskable_entities')
    op.drop_table('tasks')
