from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB, UUID
import uuid

from app.core.database import Base


class Thing(Base):
    __tablename__ = "Thingz"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        index=True,
    )
    device_id = Column(
        UUID(as_uuid=True),
        ForeignKey("Devices.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    thing_type = Column(Integer, nullable=False)
    data_type = Column(Integer, nullable=False)

    name = Column(String, nullable=True)
    unit = Column(String, nullable=True)

    slug = Column(String, nullable=False)
    hardware_address = Column(String, nullable=True, server_default="0")

    is_active = Column(Boolean, default=True)

    meta = Column(JSONB, server_default="{}")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint(
            "device_id",
            "hardware_address",
            "slug",
            name="unique_device_id_hardware_address_slug",
        ),
    )

    # device = relationship("Device", back_populates="things")
    # thing_card = relationship("ThingCard", back_populates="thing")
