import enum

from sqlalchemy import Column, text, func, String, Enum, ForeignKey
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_utils import UUIDType, ArrowType, generic_repr

from ingredients_db.database import Base


class ProjectState(enum.Enum):
    CREATED = 'CREATED'
    DELETING = 'DELETING'
    DELETED = 'DELETED'
    ERROR = 'ERROR'


# TODO: project members (users)
# only project members can do things within the project


@generic_repr
class Project(Base):
    __tablename__ = 'projects'

    id = Column(UUIDType, server_default=text("uuid_generate_v4()"), primary_key=True)
    name = Column(String, unique=True, nullable=False)
    state = Column(Enum(ProjectState), default=ProjectState.CREATED, nullable=False)

    created_at = Column(ArrowType(timezone=True), server_default=func.now(), nullable=False, index=True)
    updated_at = Column(ArrowType(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class ProjectMixin(object):
    @declared_attr
    def project_id(cls):
        return Column(UUIDType, ForeignKey('projects.id', ondelete='RESTRICT'), nullable=False)
