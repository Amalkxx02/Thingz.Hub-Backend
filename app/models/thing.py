from sqlalchemy import (
    CheckConstraint,
    Column,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.database.base import Base

class Thing(Base):
    __tablename__ = "Things"
    thing_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    device_id = Column(UUID(as_uuid=True), ForeignKey("Devices.device_id", ondelete="CASCADE"), nullable=False)
    thing_type = Column(String, nullable=False)
    thing_name = Column(String, nullable=False)

    device = relationship("Device", back_populates="things")
    thing_card = relationship("ThingCard", back_populates="thing")

    __table_args__ = (
        UniqueConstraint("device_id", "thing_name", name="unique_device_id_thing_name"),
        CheckConstraint(thing_type.in_(["sensor", "actuator"]), name="allow_sensor_or_actuator"),
    )