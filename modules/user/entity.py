from sqlalchemy import Column, String, String
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(String, nullable=False, primary_key=True)
    username = Column(String(255), nullable=False)
    card_number = Column(String(16), nullable=True)
    email = Column(String(255), nullable=False, unique=True)
    
    history_entries = relationship("History", back_populates="user")
    attendants = relationship("Attendance", back_populates="user")
    # Smart lock relationships
    lock_permissions = relationship("LockPermission", back_populates="user")
    lock_access_logs = relationship("LockAccessLog", back_populates="user")