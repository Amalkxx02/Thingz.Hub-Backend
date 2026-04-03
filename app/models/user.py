from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    DateTime,
    Boolean
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

from app.database.base import Base


class User(Base):
    __tablename__ = "Users"
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("Auths.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    profile_image_url = Column(String, nullable=True)
    is_onboarded = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # devices = relationship("Device", back_populates="user")
    # things_card = relationship("ThingCard", back_populates="user")
