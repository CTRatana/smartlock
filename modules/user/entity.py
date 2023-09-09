from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from core.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    
    cards = relationship("Card", back_populates="user")
    history_entries = relationship("History", back_populates="user")
    attendants = relationship("Attendant", back_populates="user")