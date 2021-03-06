import enum

from sqlalchemy import text, Column, String, Enum, Text, ForeignKey
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_utils import UUIDType, ArrowType, generic_repr

from ingredients_db.database import Base


class TaskState(enum.Enum):
    PENDING = 'PENDING'
    RUNNING = 'RUNNING'
    COMPLETED = 'COMPLETED'
    ERROR = 'ERROR'


@generic_repr
class Task(Base):
    __tablename__ = 'tasks'

    id = Column(UUIDType, server_default=text("uuid_generate_v4()"), primary_key=True)
    name = Column(String, nullable=False)
    state = Column(Enum(TaskState), default=TaskState.PENDING, nullable=False)
    error_message = Column(Text)

    created_at = Column(ArrowType(timezone=True), server_default=text('clock_timestamp()'), nullable=False, index=True)
    updated_at = Column(ArrowType(timezone=True), server_default=text('clock_timestamp()'),
                        onupdate=text('clock_timestamp()'), nullable=False)
    stopped_at = Column(ArrowType(timezone=True))


class TaskMixin(object):
    @declared_attr
    def current_task_id(cls):
        return Column(UUIDType, ForeignKey('tasks.id'))
