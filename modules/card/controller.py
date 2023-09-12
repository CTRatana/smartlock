from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from modules.card.model import CardInsertRequest, CardUpdateRequest
from db import get_db
from modules.card.entity import Card

router = APIRouter(
    prefix='/Card',
    tags=['Card']
)

@router.post('')
def create(item: CardInsertRequest, db: Session = Depends(get_db)):
    db_item = Card(card_number=item.card_number, user_id=item.user_id)
    db.add(db_item)
    db.commit()
    return db_item
   
@router.get('')
def gets(db: Session =  Depends(get_db)):
    return db.query(Card).all()

@router.get('/{item_id}')
def get(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Card).filter(Card.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail='Item not found')
    return item

@router.put('/{item_id}')
def update(item_id: int, item: CardUpdateRequest, db: Session = Depends(get_db)):
    old = db.query(Card).filter(Card.id == item_id).first()
    if old is None:
        raise HTTPException(status_code=404, detail='Item not found')
    old.card_number = item.card_number
    db.commit()
    return old

@router.delete('/{item_id}')
def delete(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Card).filter(Card.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail='Item not found')
    db.delete(item)
    db.commit()
    return item