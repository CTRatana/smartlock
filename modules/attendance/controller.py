from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from modules.attendance.model import AttendanceInsertRequest
from core.database import get_db
from modules.attendance.entity import Attendance

router = APIRouter(
    prefix='/Attendance',
    tags=['Attendance']
)

@router.post('')
def create(item:AttendanceInsertRequest,db: Session = Depends(get_db)):
    db_item = Attendance(user_id=item.user_id)
    db.add(db_item)
    db.commit()
    return db_item
   
@router.get('')
def gets(db: Session =  Depends(get_db)):
    return db.query(Attendance).all()

@router.get('/{item_id}')
def get(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Attendance).filter(Attendance.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail='Item not found')
    return item

