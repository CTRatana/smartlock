from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base

class Attendance(Base):
    __tablename__ = 'attendance'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="attendants")