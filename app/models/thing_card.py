from sqlalchemy import Column, Integer, ForeignKey, JSON, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.database.base import Base

class ThingCard(Base):
    __tablename__ = "Things_Card"
    card_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("Users.user_id", ondelete="CASCADE"), nullable=False
    )
    thing_id = Column(
        Integer, ForeignKey("Things.thing_id", ondelete="CASCADE"), nullable=False, unique=True
    )
    config = Column(JSON)

    __table_args__ = (UniqueConstraint("user_id", "thing_id", name="unique_card_user_card"),)

    user = relationship("User", back_populates="things_card")
    thing = relationship("Thing", back_populates="thing_card")
