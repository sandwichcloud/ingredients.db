import enum

from sqlalchemy import Column, String, ForeignKey, Enum, text
from sqlalchemy.dialects.postgresql import HSTORE
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType, generic_repr, ArrowType

from ingredients_db.database import Base
from ingredients_db.models.authn import ServiceAccountMixin
from ingredients_db.models.keypair import Keypair
from ingredients_db.models.network_port import NetworkableMixin
from ingredients_db.models.project import ProjectMixin
from ingredients_db.models.region import RegionableNixin
from ingredients_db.models.task import TaskMixin
from ingredients_db.models.zones import ZonableMixin


class InstanceState(enum.Enum):
    BUILDING = 'BUILDING'
    ACTIVE = 'ACTIVE'
    STARTING = 'STARTING'
    RESTARTING = 'RESTARTING'
    STOPPING = 'STOPPING'
    STOPPED = 'STOPPED'
    DELETING = 'DELETING'
    DELETED = 'DELETED'
    IMAGING = 'IMAGING'
    ERROR = 'ERROR'


@generic_repr
class Instance(Base, TaskMixin, NetworkableMixin, ProjectMixin, RegionableNixin, ZonableMixin, ServiceAccountMixin):
    __tablename__ = 'instances'

    id = Column(UUIDType, server_default=text("uuid_generate_v4()"), primary_key=True)
    name = Column(String, nullable=False)
    tags = Column(HSTORE)
    state = Column(Enum(InstanceState), default=InstanceState.BUILDING, nullable=False)

    image_id = Column(UUIDType, ForeignKey('images.id', ondelete='SET NULL'))

    keypairs = relationship(Keypair, secondary='instance_keypairs')

    created_at = Column(ArrowType(timezone=True), server_default=text('clock_timestamp()'), nullable=False, index=True)
    updated_at = Column(ArrowType(timezone=True), server_default=text('clock_timestamp()'),
                        onupdate=text('clock_timestamp()'), nullable=False)


class InstanceKeypair(Base):
    __tablename__ = 'instance_keypairs'

    id = Column(UUIDType, server_default=text("uuid_generate_v4()"), primary_key=True)

    keypair_id = Column(UUIDType, ForeignKey('keypairs.id', ondelete='CASCADE'))
    instance_id = Column(UUIDType, ForeignKey('instances.id', ondelete='CASCADE'))

    created_at = Column(ArrowType(timezone=True), server_default=text('clock_timestamp()'), nullable=False, index=True)
    updated_at = Column(ArrowType(timezone=True), server_default=text('clock_timestamp()'),
                        onupdate=text('clock_timestamp()'), nullable=False)
