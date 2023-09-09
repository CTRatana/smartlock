from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from modules.card.model import CardInsertRequest, CardUpdateRequest
from core.database import get_db
from modules.card.entity import Card

router = APIRouter(
    prefix='/Card',
    tags=['Card']
)

@router.post('')
def create(item: CardInsertRequest, db: Session = Depends(get_db)):
    db_item = Card(name=item.name)
    db.add(db_item)
    db.commit()
    return db_item
   
@router.get('')
def gets(db: Session =  Depends(get_db)):
    return db.query(Card).all()