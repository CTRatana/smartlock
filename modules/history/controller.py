import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from modules.history.model import HistoryInsertRequest
from database import get_db
from modules.history.entity import History

router = APIRouter(
    prefix='/History',
    tags=['History']
)

@router.post('')
def create(item: HistoryInsertRequest, db: Session = Depends(get_db)):
    existing_item = db.query(History).filter(
        History.user_id == item.user_id,
        History.date == item.date
    ).first()

    if existing_item:
        return "Item already exists"
    
    db_item = History(user_id=item.user_id)
    db.add(db_item)
    db.commit()

    return "S"
   
@router.get('')
def gets(db: Session = Depends(get_db)):
    items = db.query(History).all()
    result = [
        History(id=item.id, user_id=item.user_id, date=item.date) for item in items
    ]
    return result 

@router.get('/GetById/{item_id}')
def get(item_id: str, db: Session = Depends(get_db)):
    item = db.query(History).filter(History.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail='Item not found')
    return item

@router.get('/GetByUserId/{user_id}')
def get(user_id: str, db: Session = Depends(get_db)):
    item = db.query(History).filter(History.user_id == user_id).all()
    if item is None:
        raise HTTPException(status_code=404, detail='Item not found')
    return item