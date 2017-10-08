import enum

from sqlalchemy import Column, String, ForeignKey, Enum, text, func
from sqlalchemy.dialects.postgresql import HSTORE
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType, generic_repr, ArrowType

from ingredients_db.database import Base
from ingredients_db.models.network_port import NetworkableEntity
from ingredients_db.models.public_key import PublicKey


class InstanceState(enum.Enum):
    BUILDING = 'BUILDING'
    ACTIVE = 'ACTIVE'
    STARTING = 'STARTING'
    RESTARTING = 'RESTARTING'
    STOPPING = 'STOPPING'
    STOPPED = 'STOPPED'
    DELETING = 'DELETING'
    DELETED = 'DELETED'
    ERROR = 'ERROR'


@generic_repr
class Instance(NetworkableEntity):
    __tablename__ = 'instances'

    id = Column(UUIDType, ForeignKey('networkable_entities.id'), primary_key=True)
    name = Column(String, nullable=False)
    tags = Column(HSTORE)
    state = Column(Enum(InstanceState), default=InstanceState.BUILDING, nullable=False)

    project_id = Column(UUIDType, ForeignKey('projects.id', ondelete='RESTRICT'), nullable=False)
    image_id = Column(UUIDType, ForeignKey('images.id', ondelete='SET NULL'))

    public_keys = relationship(PublicKey, secondary='instance_public_keys')

    __mapper_args__ = {
        'polymorphic_identity': 'instance'
    }


class InstancePublicKey(Base):
    __tablename__ = 'instance_public_keys'

    id = Column(UUIDType, server_default=text("uuid_generate_v4()"), primary_key=True)

    public_key_id = Column(UUIDType, ForeignKey('public_keys.id', ondelete='CASCADE'))
    instance_id = Column(UUIDType, ForeignKey('instances.id', ondelete='CASCADE'))

    created_at = Column(ArrowType(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(ArrowType(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
