from sqlalchemy import TIMESTAMP, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base

class History(Base):
    __tablename__ = 'history'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    user_id = Column(UUID, ForeignKey('users.id'))

    user = relationship("User", back_populates="history_entries")