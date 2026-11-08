from sqlalchemy import Column, ForeignKey, LargeBinary, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class Token(Base):
    __tablename__ = "Tokens"
    jti = Column(UUID(as_uuid=True), primary_key=True, nullable=False, index=True)
    sub = Column(
        UUID(as_uuid=True), ForeignKey("Auths.id", ondelete="CASCADE"), nullable=False
    )
    iat = Column(DateTime(timezone=True), nullable=False)
    exp = Column(DateTime(timezone=True), nullable=False)
    is_revoked = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
