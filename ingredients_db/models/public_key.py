from sqlalchemy import text, Column, String, Text, func
from sqlalchemy_utils import UUIDType, generic_repr, ArrowType

from ingredients_db.database import Base
from ingredients_db.models.project import ProjectMixin


@generic_repr
class PublicKey(Base, ProjectMixin):
    __tablename__ = 'public_keys'

    id = Column(UUIDType, server_default=text("uuid_generate_v4()"), primary_key=True)
    name = Column(String, nullable=False)
    key = Column(Text, nullable=False)

    created_at = Column(ArrowType(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(ArrowType(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
