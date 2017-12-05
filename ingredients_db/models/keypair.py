from sqlalchemy import text, Column, String, Text, ForeignKey
from sqlalchemy_utils import UUIDType, generic_repr, ArrowType

from ingredients_db.database import Base


@generic_repr
class Keypair(Base):
    __tablename__ = 'keypairs'

    id = Column(UUIDType, server_default=text("uuid_generate_v4()"), primary_key=True)
    name = Column(String, nullable=False)
    public_key = Column(Text, nullable=False)

    project_id = Column(UUIDType, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)

    created_at = Column(ArrowType(timezone=True), server_default=text('clock_timestamp()'), nullable=False, index=True)
    updated_at = Column(ArrowType(timezone=True), server_default=text('clock_timestamp()'),
                        onupdate=text('clock_timestamp()'), nullable=False)
