import enum
import ipaddress
from typing import Optional

from sqlalchemy import Column, String, Enum, ForeignKey
from sqlalchemy_utils import UUIDType, generic_repr, IPAddressType

from ingredients_db.models.network_port import NetworkPort
from ingredients_db.models.task import TaskableEntity
from ingredients_db.types import IPv4Network


class NetworkState(enum.Enum):
    CREATING = 'CREATING'
    CREATED = 'CREATED'
    DELETING = 'DELETING'
    DELETED = 'DELETED'
    ERROR = 'ERROR'


@generic_repr
class Network(TaskableEntity):
    __tablename__ = 'networks'

    id = Column(UUIDType, ForeignKey('taskable_entities.id'), primary_key=True)
    name = Column(String, unique=True, nullable=False)

    port_group = Column(String, unique=True, nullable=False)

    state = Column(Enum(NetworkState), default=NetworkState.CREATING, nullable=False)

    cidr = Column(IPv4Network, nullable=False)
    pool_start = Column(IPAddressType, nullable=False)
    pool_end = Column(IPAddressType, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'network'
    }

    def next_free_address(self, session) -> Optional[ipaddress.IPv4Address]:
        ip_network = ipaddress.ip_network(self.cidr)

        ip_addresses = []

        for host in ip_network.hosts():
            start_host = ipaddress.IPv4Address(self.pool_start)
            end_host = ipaddress.IPv4Address(self.pool_end)

            if start_host <= host <= end_host:
                ip_addresses.append(host)

        network_ports = session.query(NetworkPort).filter(NetworkPort.network_id == self.id).filter(
            NetworkPort.ip_address != None).with_for_update()  # noqa: ignore=E711

        for network_port in network_ports:
            ip_address = ipaddress.IPv4Address(network_port.ip_address)
            if ip_address in ip_addresses:
                ip_addresses.remove(ip_address)

        if len(ip_addresses) > 0:
            return ip_addresses[0]

        return None
