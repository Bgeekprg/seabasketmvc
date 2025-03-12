from sqlalchemy import Column, String, DateTime, ForeignKey
from config.db_config import Base
from datetime import datetime, timezone


class ResetToken(Base):
    __tablename__ = "reset_tokens"

    token = Column(String(255), primary_key=True, index=True)
    email = Column(String(255), ForeignKey("users.email"), nullable=False)
    expires = Column(DateTime, nullable=False)

    def is_expired(self):
        return datetime.now(timezone.utc) > self.expires
