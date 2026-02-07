"""
models.py
----------
SQLAlchemy ORM models for the IoT Dashboard system.

Tables:
- Users: Stores user credentials and profile data. `uuid` used to generate `user_id`.
- Devices: IoT devices registered under each user. `uuid` used to generate `device_id`.
- Things: Individual sensors or actuators associated with devices.
- User_Things_Cards: UI cards on user dashboards for displaying or controlling Things.
- Rooms: Logical grouping of Things (user's room setup). (Currently disabled.)

Relationships:
- User → Devices → Things
- User → Rooms
- Things ↔ User_Things_Cards

Notes:
- Future:
    - Implement Room support.
    - Possibly add new columns (e.g., device metadata, thing properties).
"""

from sqlalchemy import (
    Column, Integer, String, LargeBinary, DateTime,
    ForeignKey, JSON, UniqueConstraint, CheckConstraint
)
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid

# --------------------------
# Database Initialization
# --------------------------

sync_database_url = "postgresql+psycopg2://iot_admin:1234@localhost/iot_dashboard"
sync_engine = create_engine(sync_database_url)
Base = declarative_base()

# --------------------------
# Models
# --------------------------

class User(Base):
    """Represents a user account in the IoT Dashboard."""

    __tablename__ = "Users"
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False, index=True)
    user_name = Column(String, nullable=False)
    user_email = Column(String, unique=True, nullable=False)
    user_password = Column(LargeBinary, nullable=False)  # Hashed password
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    devices = relationship("Device", back_populates="user")
    # rooms = relationship("Room", back_populates="user")  # Future
    things_card = relationship("ThingCard", back_populates="user")


class Device(Base):
    """Represents a physical IoT device linked to a user."""

    __tablename__ = "Devices"
    device_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("Users.user_id", ondelete="CASCADE"), nullable=False)
    device_name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "device_name", name="unique_device_name_for_each_user"),
    )

    # Relationships
    things = relationship("Thing", back_populates="device")
    user = relationship("User", back_populates="devices")


class Thing(Base):
    """Represents a sensor or actuator on a device."""

    __tablename__ = "Things"
    thing_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    device_id = Column(UUID(as_uuid=True), ForeignKey("Devices.device_id", ondelete="CASCADE"), nullable=False)
    thing_type = Column(String, nullable=False)
    thing_name = Column(String, nullable=False)

    # Relationships
    device = relationship("Device", back_populates="things")
    thing_card = relationship("ThingCard", back_populates="thing")

    __table_args__ = (
        UniqueConstraint("device_id", "thing_name", name="unique_device_id_thing_name"),
        CheckConstraint(thing_type.in_(["sensor", "actuator"]), name="allow_sensor_or_actuator"),
    )


class ThingCard(Base):
    """Represents a dashboard card for a user's Thing."""

    __tablename__ = "Things_Card"
    card_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("Users.user_id", ondelete="CASCADE"), nullable=False)
    thing_id = Column(Integer, ForeignKey("Things.thing_id", ondelete="CASCADE"), nullable=False, unique=True)
    config = Column(JSON)  # Stores layout, color, thresholds, etc.

    __table_args__ = (
        UniqueConstraint("user_id", "thing_id", name="unique_card_user_card"),
    )

    # Relationships
    user = relationship("User", back_populates="things_card")
    thing = relationship("Thing", back_populates="thing_card")


"""
# Future Room Implementation

class Room(Base):
    Represents a user's room for organizing Things.

    __tablename__ = "Rooms"
    room_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("Users.user_id", ondelete="CASCADE"), nullable=False)
    room_name = Column(String, nullable=False)
    room_color = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "room_name", name="unique_user_room"),
    )

    user = relationship("User", back_populates="rooms")
"""

# --------------------------
# Create Tables
# --------------------------

Base.metadata.create_all(sync_engine)
