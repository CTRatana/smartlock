from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from modules.history.model import HistoryListResponse, HistoryInsertRequest
from db import get_db
from modules.history.entity import History

router = APIRouter(
    prefix='/History',
    tags=['History']
)

@router.post('')
def create(item: HistoryInsertRequest,db: Session = Depends(get_db)):
    db_item = History(user_id=item.user_id)
    db.add(db_item)
    db.commit()
    return db_item
   
@router.get('')
def gets(db: Session = Depends(get_db)):
    items = db.query(History).all()
    result = [] 
    for item in items:
        response_item = HistoryListResponse(
            id=item.id,
            date=item.date,
            user_id=item.user_id
        )
        result.append(response_item)
    return result 

@router.get('/{item_id}')
def get(item_id: int, db: Session = Depends(get_db)):
    item = db.query(History).filter(History.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail='Item not found')
    return item