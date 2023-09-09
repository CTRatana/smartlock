from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from modules.user.model import UserInsertRequest, UserUpdateRequest
from core.database import get_db
from modules.user.entity import User

router = APIRouter(
    prefix='/User',
    tags=['User']
)

@router.post('')
def create(item: UserInsertRequest, db: Session = Depends(get_db)):
    db_item = User(name=item.name)
    db.add(db_item)
    db.commit()
    return db_item
   
@router.get('')
def gets(db: Session =  Depends(get_db)):
    return db.query(User).all()