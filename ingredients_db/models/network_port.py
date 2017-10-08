from sqlalchemy import Column, text, func, ForeignKey
from sqlalchemy_utils import UUIDType, ArrowType, generic_repr, IPAddressType

from ingredients_db.database import Base
from ingredients_db.models.task import TaskableEntity


@generic_repr
class NetworkPort(Base):
    __tablename__ = 'network_ports'

    id = Column(UUIDType, server_default=text("uuid_generate_v4()"), primary_key=True)

    network_id = Column(UUIDType, ForeignKey('networks.id', ondelete='RESTRICT'), nullable=False)
    ip_address = Column(IPAddressType)

    created_at = Column(ArrowType(timezone=True), server_default=func.now(), nullable=False, index=True)
    updated_at = Column(ArrowType(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


@generic_repr
class NetworkableEntity(TaskableEntity):
    __tablename__ = 'networkable_entities'

    id = Column(UUIDType, ForeignKey('taskable_entities.id'), primary_key=True)
    network_port_id = Column(UUIDType, ForeignKey('network_ports.id', ondelete='SET NULL'))

    __mapper_args__ = {
        'polymorphic_identity': 'networkable_entity'
    }
