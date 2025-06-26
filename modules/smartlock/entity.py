from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class Lock(Base):
    __tablename__ = 'locks'

    id = Column(String, primary_key=True)
    name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    status = Column(Boolean, default=False)  # False = locked, True = unlocked
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Define permissions for users
    access_logs = relationship("LockAccessLog", back_populates="lock")
    permissions = relationship("LockPermission", back_populates="lock")


class LockPermission(Base):
    __tablename__ = 'lock_permissions'

    id = Column(String, primary_key=True)
    lock_id = Column(String, ForeignKey('locks.id'), nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    can_unlock = Column(Boolean, default=True)
    can_manage = Column(Boolean, default=False)  # Can manage lock settings and permissions
    
    lock = relationship("Lock", back_populates="permissions")
    user = relationship("User")


class LockAccessLog(Base):
    __tablename__ = 'lock_access_logs'

    id = Column(String, primary_key=True)
    lock_id = Column(String, ForeignKey('locks.id'), nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=True)  # Nullable for failed access attempts
    action = Column(String(50), nullable=False)  # unlock, lock, failed_attempt
    timestamp = Column(DateTime, server_default=func.now())
    
    lock = relationship("Lock", back_populates="access_logs")
    user = relationship("User")