from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from modules.attendance.model import AttendanceInsertRequest, AttendanceUpdateRequest
from core.database import get_db
from modules.attendance.entity import Attendance

router = APIRouter(
    prefix='/Attendance',
    tags=['Attendance']
)

@router.post('')
def create(item: AttendanceInsertRequest, db: Session = Depends(get_db)):
    db_item = Attendance(name=item.name)
    db.add(db_item)
    db.commit()
    return db_item
   
@router.get('')
def gets(db: Session =  Depends(get_db)):
    return db.query(Attendance).all()