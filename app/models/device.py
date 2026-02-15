from sqlalchemy import Column, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.database.base import Base

class Device(Base):
    __tablename__ = "Devices"
    device_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("Users.user_id", ondelete="CASCADE"), nullable=False)
    device_name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "device_name", name="unique_device_name_for_each_user"),
    )
    things = relationship("Thing", back_populates="device")
    user = relationship("User", back_populates="devices")