import enum

from sqlalchemy import Column, text, String, Enum, ForeignKey
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_utils import UUIDType, ArrowType, generic_repr

from ingredients_db.database import Base


class ProjectState(enum.Enum):
    CREATED = 'CREATED'
    DELETING = 'DELETING'
    DELETED = 'DELETED'
    ERROR = 'ERROR'


@generic_repr
class Project(Base):
    __tablename__ = 'projects'

    id = Column(UUIDType, server_default=text("uuid_generate_v4()"), primary_key=True)
    name = Column(String, unique=True, nullable=False)
    state = Column(Enum(ProjectState), default=ProjectState.CREATED, nullable=False)

    created_at = Column(ArrowType(timezone=True), server_default=text('clock_timestamp()'), nullable=False, index=True)
    updated_at = Column(ArrowType(timezone=True), server_default=text('clock_timestamp()'),
                        onupdate=text('clock_timestamp()'), nullable=False)


class ProjectMixin(object):
    @declared_attr
    def project_id(cls):
        return Column(UUIDType, ForeignKey('projects.id', ondelete='RESTRICT'), nullable=False)


@generic_repr
class ProjectMembers(Base):
    __tablename__ = 'project_members'

    id = Column(UUIDType, server_default=text("uuid_generate_v4()"), primary_key=True)
    user_id = Column(UUIDType, ForeignKey('authn_users.id', ondelete='CASCADE'), nullable=False, index=True)
    role_id = Column(UUIDType, ForeignKey('authz_roles.id', ondelete='RESTRICT'), nullable=False, index=True)
    project_id = Column(UUIDType, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False, index=True)

    created_at = Column(ArrowType(timezone=True), server_default=text('clock_timestamp()'), nullable=False, index=True)
    updated_at = Column(ArrowType(timezone=True), server_default=text('clock_timestamp()'),
                        onupdate=text('clock_timestamp()'), nullable=False)
