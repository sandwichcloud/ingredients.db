from sqlalchemy import String, Column, text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy_utils import ArrowType, UUIDType, PasswordType

from ingredients_db.database import Base


class BuiltInUser(Base):
    __tablename__ = 'builtin_users'

    id = Column(UUIDType, server_default=text("uuid_generate_v4()"), primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(PasswordType(schemes=['bcrypt']), nullable=False)
    roles = Column(ARRAY(String), default=list)

    created_at = Column(ArrowType(timezone=True), server_default=text('clock_timestamp()'), nullable=False, index=True)
    updated_at = Column(ArrowType(timezone=True), server_default=text('clock_timestamp()'),
                        onupdate=text('clock_timestamp()'), nullable=False)
