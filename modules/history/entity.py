from sqlalchemy import TIMESTAMP, Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base

class History(Base):
    __tablename__ = 'history'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    user_id = Column(UUID, ForeignKey('users.id'))

    user = relationship("User", back_populates="history_entries")