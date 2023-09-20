from sqlalchemy import Column, Date, ForeignKey, Integer, String

from sqlalchemy.orm import relationship

from database import Base

class History(Base):
    __tablename__ = 'history'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    user_id = Column(String, ForeignKey('users.id'))

    user = relationship("User", back_populates="history_entries")