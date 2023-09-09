from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from modules.history.model import HistoryInsertRequest, HistoryUpdateRequest
from core.database import get_db
from modules.history.entity import History

router = APIRouter(
    prefix='/History',
    tags=['History']
)

@router.post('')
def create(item: HistoryInsertRequest, db: Session = Depends(get_db)):
    db_item = History(name=item.name)
    db.add(db_item)
    db.commit()
    return db_item
   
@router.get('')
def gets(db: Session =  Depends(get_db)):
    return db.query(History).all()