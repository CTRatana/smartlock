from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False)
    card_number = Column(String(16), nullable=True)
    email = Column(String(255), nullable=False, unique=True)
    
    history_entries = relationship("History", back_populates="user")
    attendants = relationship("Attendance", back_populates="user")