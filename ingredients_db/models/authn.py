from sqlalchemy import Column, String, text, UniqueConstraint, ForeignKey
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_utils import ArrowType, UUIDType

from ingredients_db.database import Base


class AuthNUser(Base):
    __tablename__ = 'authn_users'

    __table_args__ = (
        UniqueConstraint('username', 'driver', name='uq_username_driver'),
    )

    id = Column(UUIDType, server_default=text("uuid_generate_v4()"), primary_key=True)
    username = Column(String, nullable=False)
    driver = Column(String, nullable=False)

    created_at = Column(ArrowType(timezone=True), server_default=text('clock_timestamp()'), nullable=False, index=True)
    updated_at = Column(ArrowType(timezone=True), server_default=text('clock_timestamp()'),
                        onupdate=text('clock_timestamp()'), nullable=False)


# TODO: should we have locked service accounts to prevent accidental deletion/modification?
# i.e the default instance service account
class AuthNServiceAccount(Base):
    __tablename__ = 'authn_service_accounts'

    id = Column(UUIDType, server_default=text("uuid_generate_v4()"), primary_key=True)
    name = Column(String, nullable=False)
    project_id = Column(UUIDType, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    role_id = Column(UUIDType, ForeignKey('authz_roles.id', ondelete='RESTRICT'), nullable=False)

    created_at = Column(ArrowType(timezone=True), server_default=text('clock_timestamp()'), nullable=False, index=True)
    updated_at = Column(ArrowType(timezone=True), server_default=text('clock_timestamp()'),
                        onupdate=text('clock_timestamp()'), nullable=False)


class ServiceAccountMixin(object):
    @declared_attr
    def service_account_id(cls):
        return Column(UUIDType, ForeignKey('authn_service_accounts.id', ondelete='RESTRICT'), nullable=False)
