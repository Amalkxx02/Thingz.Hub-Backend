from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    LargeBinary,
    String,
    Index,
    text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.core.database import Base


class Device(Base):
    __tablename__ = "Devices"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        index=True,
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("Users.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name = Column(String, nullable=False)
    type = Column(Integer, nullable=False)
    mac_address = Column(String, nullable=True)
    firmware = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)

    hashed_key = Column(LargeBinary, nullable=False, index=True)
    key_hint = Column(String, nullable=False)

    is_revoked = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=False, nullable=False)
    is_registered = Column(Boolean, default=False, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index("unique_mac_address","mac_address",unique=True,postgresql_where=text("mac_address IS NOT NULL")),
    )
    # things = relationship("Thing", back_populates="device")
    # user = relationship("User", back_populates="devices")
