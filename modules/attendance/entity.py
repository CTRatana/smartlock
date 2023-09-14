from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base

class Attendance(Base):
    __tablename__ = 'attendance'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(TIMESTAMP, nullable=False)
    user_id = Column(UUID, ForeignKey('users.id'))

    user = relationship("User", back_populates="attendants")