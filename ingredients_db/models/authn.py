import arrow
from sqlalchemy import Column, String, text, ForeignKey, UniqueConstraint
from sqlalchemy_utils import generic_repr, ArrowType, UUIDType

from ingredients_db.database import Base


class AuthNUser(Base):
    __tablename__ = 'authn_users'

    __table_args__ = (
        UniqueConstraint('username', 'driver', name='uq_username_driver'),
    )

    id = Column(UUIDType, server_default=text("uuid_generate_v4()"), primary_key=True)
    username = Column(String, nullable=False)
    driver = Column(String, nullable=False)

    created_at = Column(ArrowType(timezone=True), server_default=text('clock_timestamp()'), nullable=False)
    updated_at = Column(ArrowType(timezone=True), server_default=text('clock_timestamp()'),
                        onupdate=text('clock_timestamp()'), nullable=False)


@generic_repr
class AuthNToken(Base):
    __tablename__ = 'authn_tokens'

    id = Column(UUIDType, server_default=text("uuid_generate_v4()"), primary_key=True)
    access_token = Column(String, nullable=False, index=True)

    user_id = Column(UUIDType, ForeignKey('authn_users.id', ondelete='CASCADE'), nullable=False)
    project_id = Column(UUIDType, ForeignKey('projects.id', ondelete='CASCADE'))

    created_at = Column(ArrowType(timezone=True), server_default=text('clock_timestamp()'), nullable=False, index=True)
    updated_at = Column(ArrowType(timezone=True), server_default=text('clock_timestamp()'),
                        onupdate=text('clock_timestamp()'), nullable=False)
    expires_at = Column(ArrowType(timezone=True), default=arrow.now().shift(days=+1), nullable=False)


class AuthNTokenRole(Base):
    __tablename__ = 'authn_token_roles'

    id = Column(UUIDType, server_default=text("uuid_generate_v4()"), primary_key=True)
    token_id = Column(UUIDType, ForeignKey('authn_tokens.id', ondelete='CASCADE'), nullable=False)
    role_id = Column(UUIDType, ForeignKey('authz_roles.id', ondelete='CASCADE'), nullable=False)

    created_at = Column(ArrowType(timezone=True), server_default=text('clock_timestamp()'), nullable=False, index=True)
    updated_at = Column(ArrowType(timezone=True), server_default=text('clock_timestamp()'),
                        onupdate=text('clock_timestamp()'), nullable=False)
