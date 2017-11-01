import enum

from sqlalchemy import Column, String, ForeignKey, Enum, Boolean, text
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType, ArrowType, generic_repr

from ingredients_db.database import Base
from ingredients_db.models.project import Project, ProjectMixin
from ingredients_db.models.task import TaskMixin


class ImageState(enum.Enum):
    CREATING = 'CREATING'
    CREATED = 'CREATED'
    DELETING = 'DELETING'
    DELETED = 'DELETED'
    ERROR = 'ERROR'


class ImageVisibility(enum.Enum):
    PUBLIC = 'PUBLIC'
    SHARED = 'SHARED'
    PRIVATE = 'PRIVATE'


@generic_repr
class ImageMembers(Base):
    __tablename__ = 'image_members'

    image_id = Column(UUIDType, ForeignKey('images.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    project_id = Column(UUIDType, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False, primary_key=True)

    created_at = Column(ArrowType(timezone=True), server_default=text('clock_timestamp()'), nullable=False, index=True)


# TODO: Image families

@generic_repr
class Image(Base, TaskMixin, ProjectMixin):
    __tablename__ = 'images'

    id = Column(UUIDType, server_default=text("uuid_generate_v4()"), primary_key=True)
    name = Column(String, nullable=False)
    file_name = Column(String, unique=True, nullable=False)
    locked = Column(Boolean, default=False, nullable=False)

    state = Column(Enum(ImageState), default=ImageState.CREATING, nullable=False)
    visibility = Column(Enum(ImageVisibility), default=ImageVisibility.PRIVATE, nullable=False)

    created_at = Column(ArrowType(timezone=True), server_default=text('clock_timestamp()'), nullable=False, index=True)
    updated_at = Column(ArrowType(timezone=True), server_default=text('clock_timestamp()'),
                        onupdate=text('clock_timestamp()'), nullable=False)

    members = relationship(Project, secondary='image_members')
