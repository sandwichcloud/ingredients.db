from sqlalchemy import Column, text, ForeignKey
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_utils import UUIDType, ArrowType, generic_repr, IPAddressType

from ingredients_db.database import Base


@generic_repr
class NetworkPort(Base):
    __tablename__ = 'network_ports'

    id = Column(UUIDType, server_default=text("uuid_generate_v4()"), primary_key=True)

    network_id = Column(UUIDType, ForeignKey('networks.id', ondelete='RESTRICT'), nullable=False)
    ip_address = Column(IPAddressType)

    created_at = Column(ArrowType(timezone=True), server_default=text('clock_timestamp()'), nullable=False, index=True)
    updated_at = Column(ArrowType(timezone=True), server_default=text('clock_timestamp()'),
                        onupdate=text('clock_timestamp()'), nullable=False)


class NetworkableMixin(object):
    @declared_attr
    def network_port_id(cls):
        return Column(UUIDType, ForeignKey('network_ports.id', ondelete='RESTRICT'))
