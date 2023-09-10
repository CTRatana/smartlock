from sqlalchemy import Column, Integer,ForeignKey, String
from sqlalchemy.orm import relationship

from core.database import Base

class Card(Base):
    __tablename__ = 'card'

    id = Column(Integer, primary_key=True, index=True)
    card_number = Column(String(16), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="cards")