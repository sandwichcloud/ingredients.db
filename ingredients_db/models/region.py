import enum

from sqlalchemy import Column, text, String, Boolean, Enum, ForeignKey
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_utils import generic_repr, UUIDType, ArrowType

from ingredients_db.database import Base
from ingredients_db.models.task import TaskMixin


class RegionState(enum.Enum):
    CREATING = 'CREATING'
    CREATED = 'CREATED'
    DELETING = 'DELETING'
    DELETED = 'DELETED'
    ERROR = 'ERROR'


@generic_repr
class Region(Base, TaskMixin):
    __tablename__ = 'regions'

    id = Column(UUIDType, server_default=text("uuid_generate_v4()"), primary_key=True)
    name = Column(String, unique=True, nullable=False)
    datacenter = Column(String, unique=True, nullable=False)
    image_datastore = Column(String, nullable=False)
    image_folder = Column(String)
    schedulable = Column(Boolean, nullable=False)

    state = Column(Enum(RegionState), default=RegionState.CREATING, nullable=False)

    created_at = Column(ArrowType(timezone=True), server_default=text('clock_timestamp()'), nullable=False, index=True)
    updated_at = Column(ArrowType(timezone=True), server_default=text('clock_timestamp()'),
                        onupdate=text('clock_timestamp()'), nullable=False)


class RegionableNixin(object):
    @declared_attr
    def region_id(cls):
        return Column(UUIDType, ForeignKey('regions.id', ondelete='RESTRICT'), nullable=False)
