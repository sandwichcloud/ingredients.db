from sqlalchemy import text, Column, String, Text, func, ForeignKey
from sqlalchemy_utils import UUIDType, generic_repr, ArrowType

from ingredients_db.database import Base


@generic_repr
class PublicKey(Base):
    __tablename__ = 'public_keys'

    id = Column(UUIDType, server_default=text("uuid_generate_v4()"), primary_key=True)
    name = Column(String, nullable=False)
    key = Column(Text, nullable=False)

    project_id = Column(UUIDType, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)

    created_at = Column(ArrowType(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(ArrowType(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
