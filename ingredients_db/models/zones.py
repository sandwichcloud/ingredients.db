import enum

from sqlalchemy import Column, text, String, Boolean, ForeignKey, Integer, Enum
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_utils import generic_repr, UUIDType, ArrowType

from ingredients_db.database import Base
from ingredients_db.models.region import RegionableNixin
from ingredients_db.models.task import TaskMixin


class ZoneState(enum.Enum):
    CREATING = 'CREATING'
    CREATED = 'CREATED'
    DELETING = 'DELETING'
    DELETED = 'DELETED'
    ERROR = 'ERROR'


@generic_repr
class Zone(Base, TaskMixin, RegionableNixin):
    __tablename__ = 'zones'

    id = Column(UUIDType, server_default=text("uuid_generate_v4()"), primary_key=True)
    name = Column(String, unique=True, nullable=False)
    vm_cluster = Column(String, nullable=False)
    vm_datastore = Column(String, nullable=False)
    vm_folder = Column(String)
    core_provision_percent = Column(Integer, nullable=False)
    ram_provision_percent = Column(Integer, nullable=False)
    schedulable = Column(Boolean, nullable=False)

    state = Column(Enum(ZoneState), default=ZoneState.CREATING, nullable=False)

    created_at = Column(ArrowType(timezone=True), server_default=text('clock_timestamp()'), nullable=False, index=True)
    updated_at = Column(ArrowType(timezone=True), server_default=text('clock_timestamp()'),
                        onupdate=text('clock_timestamp()'), nullable=False)


class ZonableMixin(object):
    @declared_attr
    def zone_id(cls):
        return Column(UUIDType, ForeignKey('zones.id', ondelete='RESTRICT'))
