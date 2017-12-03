from sqlalchemy import text, Column, String, ForeignKey, UniqueConstraint, ARRAY
from sqlalchemy_utils import UUIDType, ArrowType

from ingredients_db.database import Base


# Policies cannot be added/deleted/modified
# These are just for storage
class AuthZPolicy(Base):
    __tablename__ = 'authz_policies'

    id = Column(UUIDType, server_default=text("uuid_generate_v4()"), primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)

    # Used to filter policies to create the default project member and service account roles
    tags = Column(ARRAY(String))

    created_at = Column(ArrowType(timezone=True), server_default=text('clock_timestamp()'), nullable=False, index=True)
    updated_at = Column(ArrowType(timezone=True), server_default=text('clock_timestamp()'),
                        onupdate=text('clock_timestamp()'), nullable=False)


# TODO: should we have locked roles to prevent accidental deletion/modification?
# i.e default admin role
class AuthZRole(Base):
    __tablename__ = 'authz_roles'

    __table_args__ = (
        UniqueConstraint('name', 'project_id', name='uq_name_project_id'),
    )

    id = Column(UUIDType, server_default=text("uuid_generate_v4()"), primary_key=True)
    name = Column(String, nullable=False)
    project_id = Column(UUIDType, ForeignKey('projects.id', ondelete='CASCADE'))
    description = Column(String)

    created_at = Column(ArrowType(timezone=True), server_default=text('clock_timestamp()'), nullable=False, index=True)
    updated_at = Column(ArrowType(timezone=True), server_default=text('clock_timestamp()'),
                        onupdate=text('clock_timestamp()'), nullable=False)


class AuthZRolePolicy(Base):
    __tablename__ = 'authz_role_policies'

    id = Column(UUIDType, server_default=text("uuid_generate_v4()"), primary_key=True)
    role_id = Column(UUIDType, ForeignKey('authz_roles.id', ondelete='CASCADE'), index=True, nullable=False)
    policy_id = Column(UUIDType, ForeignKey('authz_policies.id', ondelete='CASCADE'), index=True, nullable=False)

    created_at = Column(ArrowType(timezone=True), server_default=text('clock_timestamp()'), nullable=False, index=True)
    updated_at = Column(ArrowType(timezone=True), server_default=text('clock_timestamp()'),
                        onupdate=text('clock_timestamp()'), nullable=False)
