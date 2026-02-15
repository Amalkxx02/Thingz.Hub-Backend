from sqlalchemy import (
    Column,
    ForeignKey,
    LargeBinary,
    DateTime,
    Boolean
)
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

from app.database.base import Base

class Token(Base):
    __tablename__ = "Tokens"
    jti = Column(
        UUID(as_uuid=True), primary_key=True, nullable=False, index=True
    )
    sub = Column(UUID(as_uuid=True), ForeignKey("Auths.id", ondelete="CASCADE"), nullable=False)
    exp = Column(DateTime(timezone=True),nullable=False)
    iat = Column(DateTime(timezone=True),nullable=False)
    token_hash = Column(LargeBinary, nullable=False)
    revoked = Column(Boolean,default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
