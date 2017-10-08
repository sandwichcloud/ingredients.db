import enum

from sqlalchemy import Column, func, String, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType, ArrowType, generic_repr

from ingredients_db.database import Base
from ingredients_db.models.project import Project
from ingredients_db.models.task import TaskableEntity


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

    created_at = Column(ArrowType(timezone=True), server_default=func.now(), nullable=False, index=True)


# TODO: Image families

@generic_repr
class Image(TaskableEntity):
    __tablename__ = 'images'

    id = Column(UUIDType, ForeignKey('taskable_entities.id'), primary_key=True)

    name = Column(String, nullable=False)
    file_name = Column(String, unique=True, nullable=False)
    locked = Column(Boolean, default=False, nullable=False)

    state = Column(Enum(ImageState), default=ImageState.CREATING, nullable=False)
    visibility = Column(Enum(ImageVisibility), default=ImageVisibility.PRIVATE, nullable=False)

    project_id = Column(UUIDType, ForeignKey('projects.id', ondelete='RESTRICT'), nullable=False)

    members = relationship(Project, secondary='image_members')

    __mapper_args__ = {
        'polymorphic_identity': 'image'
    }
