import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from modules.user.model import UserInsertRequest, UserUpdateRequest
from database import get_db
from modules.user.entity import User

router = APIRouter(
    prefix='/User',
    tags=['User']
)

@router.get('')
def gets(db: Session =  Depends(get_db)):
    return db.query(User).all()

@router.get('/GetByCardNumber/{card_number}')
def get(card_number: str, db: Session = Depends(get_db)):
    item = db.query(User).filter(User.card_number == card_number).first()
    if item is None:
        raise HTTPException(status_code=404, detail='Item not found')
    return item 

@router.get('/GetById/{item_id}')
def get(item_id: str, db: Session = Depends(get_db)):
    item = db.query(User).filter(User.id == item_id).first()
    return item

@router.post('')
def create(item: UserInsertRequest, db: Session = Depends(get_db)):
    db_item = User(id=item.id,username=item.username, email=item.email, card_number=item.card_number)
    db.add(db_item)
    db.commit()
    return db_item

@router.put('/{item_id}')
def update(item_id: str, item: UserUpdateRequest, db: Session = Depends(get_db)):
    old = db.query(User).filter(User.id == item_id).first()
    if old is None:
        raise HTTPException(status_code=404, detail='Item not found')
    old.username = item.username
    old.card_number = item.card_number
    db.commit()
    return old

@router.delete('/{item_id}')
def delete(item_id: str, db: Session = Depends(get_db)):
    item = db.query(User).filter(User.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail='Item not found')
    db.delete(item)
    db.commit()
    return item