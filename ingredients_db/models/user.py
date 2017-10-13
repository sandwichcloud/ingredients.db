import arrow
from sqlalchemy import Column, text, func, String, ForeignKey
from sqlalchemy_utils import UUIDType, ArrowType, generic_repr

from ingredients_db.database import Base


# TODO: user roles
# i.e only admins can crud networks and crud projects


@generic_repr
class User(Base):
    __tablename__ = 'users'

    id = Column(UUIDType, server_default=text("uuid_generate_v4()"), primary_key=True)
    username = Column(String, unique=True, nullable=False)

    created_at = Column(ArrowType(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(ArrowType(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


@generic_repr
class UserToken(Base):
    __tablename__ = 'user_tokens'

    id = Column(UUIDType, server_default=text("uuid_generate_v4()"), primary_key=True)
    access_token = Column(String, nullable=False, index=True)

    user_id = Column(UUIDType, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    project_id = Column(UUIDType, ForeignKey('projects.id', ondelete='CASCADE'))

    created_at = Column(ArrowType(timezone=True), server_default=func.now(), nullable=False, index=True)
    updated_at = Column(ArrowType(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    expires_at = Column(ArrowType(timezone=True), default=arrow.now().shift(days=+1), nullable=False)
