from sqlalchemy import (
    Boolean,
    Column,
    String,
    LargeBinary,
    DateTime,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.database.session import Base


class Auth(Base):
    __tablename__ = "Auths"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        index=True,
    )
    email = Column(String, unique=True, nullable=False)
    password = Column(LargeBinary, nullable=False)
    verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # devices = relationship("Device", back_populates="user")
    # things_card = relationship("ThingCard", back_populates="user")
