from sqlalchemy import text, Column, func, String
from sqlalchemy_utils import UUIDType, ArrowType

from ingredients_db.database import Base


# TODO: should we have locked policies to prevent accidental deletion?
class AuthZPolicy(Base):
    __tablename__ = 'authz_policies'

    id = Column(UUIDType, server_default=text("uuid_generate_v4()"), primary_key=True)
    name = Column(String, nullable=False, unique=True)
    rule = Column(String, nullable=False)
    description = Column(String)

    created_at = Column(ArrowType(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(ArrowType(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


# TODO: should we have locked roles to prevent accidental deletion?
class AuthZRole(Base):
    __tablename__ = 'authz_roles'

    id = Column(UUIDType, server_default=text("uuid_generate_v4()"), primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)

    created_at = Column(ArrowType(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(ArrowType(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
