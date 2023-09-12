from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from modules.user.model import UserInsertRequest, UserUpdateRequest
from db import get_db
from modules.user.entity import User

router = APIRouter(
    prefix='/User',
    tags=['User']
)

@router.post('')
def create(item: UserInsertRequest, db: Session = Depends(get_db)):
    db_item = User(username=item.username, email=item.email)
    db.add(db_item)
    db.commit()
    return db_item
   
@router.get('')
def gets(db: Session =  Depends(get_db)):
    return db.query(User).all()

@router.get('/{item_id}')
def get(item_id: int, db: Session = Depends(get_db)):
    item = db.query(User).filter(User.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail='Item not found')
    return item

@router.get('/{item_id}')
def get(item_id: int, db: Session = Depends(get_db)):
    item = db.query(User).filter(User.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail='Item not found')
    return item

@router.put('/{item_id}')
def update(item_id: int, item: UserUpdateRequest, db: Session = Depends(get_db)):
    old = db.query(User).filter(User.id == item_id).first()
    if old is None:
        raise HTTPException(status_code=404, detail='Item not found')
    old.username = item.username

    db.commit()
    return old

@router.delete('/{item_id}')
def delete(item_id: int, db: Session = Depends(get_db)):
    item = db.query(User).filter(User.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail='Item not found')
    db.delete(item)
    db.commit()
    return item