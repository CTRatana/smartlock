import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from modules.attendance.model import AttendanceInsertRequest
from database import get_db
from modules.attendance.entity import Attendance

router = APIRouter(
    prefix='/Attendance',
    tags=['Attendance']
)

@router.post('')
def create(item: AttendanceInsertRequest, db: Session = Depends(get_db)):
    current_date = datetime.date.today()
    
    existing_item = db.query(Attendance).filter(
        Attendance.user_id == item.user_id,
        Attendance.date == current_date
    ).first()

    if existing_item:
        return "Item already exists"
    
    db_item = Attendance(user_id=item.user_id, date=current_date)
    db.add(db_item)
    db.commit()

    return "S"
   
@router.get('')
def gets(db: Session =  Depends(get_db)):
    return db.query(Attendance).all()

@router.get('/GetById/{item_id}')
def get(item_id: str, db: Session = Depends(get_db)):
    item = db.query(Attendance).filter(Attendance.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail='Item not found')
    return item
@router.get('/GetByUserId/{user_id}')
def get(user_id: str, db: Session = Depends(get_db)):
    item = db.query(Attendance).filter(Attendance.user_id == user_id).all()
    if item is None:
        raise HTTPException(status_code=404, detail='Item not found')
    return item

