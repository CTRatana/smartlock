from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from datetime import datetime

from core.database import Base

class History(Base):
    __tablename__ = 'history'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="history_entries")