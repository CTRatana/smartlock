import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from database import get_db
from modules.user.entity import User
from modules.smartlock.entity import Lock, LockPermission, LockAccessLog
from modules.smartlock.model import (
    LockCreate, LockUpdate, LockResponse,
    LockPermissionCreate, LockPermissionUpdate, LockPermissionResponse,
    LockAccessLogCreate, LockAccessLogResponse, LockStatusUpdate
)

router = APIRouter(
    prefix='/smartlock',
    tags=['Smart Lock']
)


# Lock endpoints
@router.get('/locks', response_model=List[LockResponse])
def get_all_locks(db: Session = Depends(get_db)):
    return db.query(Lock).all()


@router.get('/locks/{lock_id}', response_model=LockResponse)
def get_lock(lock_id: str, db: Session = Depends(get_db)):
    lock = db.query(Lock).filter(Lock.id == lock_id).first()
    if lock is None:
        raise HTTPException(status_code=404, detail='Lock not found')
    return lock


@router.post('/locks', response_model=LockResponse, status_code=status.HTTP_201_CREATED)
def create_lock(lock: LockCreate, db: Session = Depends(get_db)):
    db_lock = Lock(
        id=str(uuid.uuid4()),
        name=lock.name,
        location=lock.location,
        status=False  # Default to locked
    )
    db.add(db_lock)
    db.commit()
    db.refresh(db_lock)
    return db_lock


@router.put('/locks/{lock_id}', response_model=LockResponse)
def update_lock(lock_id: str, lock: LockUpdate, db: Session = Depends(get_db)):
    db_lock = db.query(Lock).filter(Lock.id == lock_id).first()
    if db_lock is None:
        raise HTTPException(status_code=404, detail='Lock not found')
    
    # Update only provided fields
    if lock.name is not None:
        db_lock.name = lock.name
    if lock.location is not None:
        db_lock.location = lock.location
    if lock.status is not None:
        db_lock.status = lock.status
    
    db.commit()
    db.refresh(db_lock)
    return db_lock


@router.delete('/locks/{lock_id}', response_model=LockResponse)
def delete_lock(lock_id: str, db: Session = Depends(get_db)):
    db_lock = db.query(Lock).filter(Lock.id == lock_id).first()
    if db_lock is None:
        raise HTTPException(status_code=404, detail='Lock not found')
    
    db.delete(db_lock)
    db.commit()
    return db_lock


# Lock status update endpoint
@router.post('/locks/{lock_id}/status', response_model=LockResponse)
def update_lock_status(lock_id: str, status_update: LockStatusUpdate, db: Session = Depends(get_db)):
    # Get the lock
    lock = db.query(Lock).filter(Lock.id == lock_id).first()
    if lock is None:
        raise HTTPException(status_code=404, detail='Lock not found')
    
    # Get the user
    user = db.query(User).filter(User.id == status_update.user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    
    # Check if user has permission
    permission = db.query(LockPermission).filter(
        LockPermission.lock_id == lock_id,
        LockPermission.user_id == status_update.user_id,
        LockPermission.can_unlock == True
    ).first()
    
    if permission is None:
        # Log failed access attempt
        access_log = LockAccessLog(
            id=str(uuid.uuid4()),
            lock_id=lock_id,
            user_id=status_update.user_id,
            action="failed_attempt"
        )
        db.add(access_log)
        db.commit()
        raise HTTPException(status_code=403, detail='User does not have permission to operate this lock')
    
    # Update lock status
    lock.status = status_update.status
    
    # Log access
    action = "unlock" if status_update.status else "lock"
    access_log = LockAccessLog(
        id=str(uuid.uuid4()),
        lock_id=lock_id,
        user_id=status_update.user_id,
        action=action
    )
    db.add(access_log)
    
    db.commit()
    db.refresh(lock)
    return lock


# Lock access by card number
@router.post('/access/card/{card_number}/{lock_id}', response_model=LockResponse)
def access_by_card(card_number: str, lock_id: str, db: Session = Depends(get_db)):
    # Get the lock
    lock = db.query(Lock).filter(Lock.id == lock_id).first()
    if lock is None:
        raise HTTPException(status_code=404, detail='Lock not found')
    
    # Get the user by card number
    user = db.query(User).filter(User.card_number == card_number).first()
    if user is None:
        # Log failed access attempt
        access_log = LockAccessLog(
            id=str(uuid.uuid4()),
            lock_id=lock_id,
            user_id=None,
            action="failed_attempt_invalid_card"
        )
        db.add(access_log)
        db.commit()
        raise HTTPException(status_code=404, detail='User not found')
    
    # Check if user has permission
    permission = db.query(LockPermission).filter(
        LockPermission.lock_id == lock_id,
        LockPermission.user_id == user.id,
        LockPermission.can_unlock == True
    ).first()
    
    if permission is None:
        # Log failed access attempt
        access_log = LockAccessLog(
            id=str(uuid.uuid4()),
            lock_id=lock_id,
            user_id=user.id,
            action="failed_attempt_no_permission"
        )
        db.add(access_log)
        db.commit()
        raise HTTPException(status_code=403, detail='User does not have permission to operate this lock')
    
    # Toggle lock status
    lock.status = not lock.status
    
    # Log access
    action = "unlock" if lock.status else "lock"
    access_log = LockAccessLog(
        id=str(uuid.uuid4()),
        lock_id=lock_id,
        user_id=user.id,
        action=action
    )
    db.add(access_log)
    
    db.commit()
    db.refresh(lock)
    return lock


# Lock permissions endpoints
@router.get('/permissions', response_model=List[LockPermissionResponse])
def get_all_permissions(db: Session = Depends(get_db)):
    return db.query(LockPermission).all()


@router.get('/permissions/lock/{lock_id}', response_model=List[LockPermissionResponse])
def get_lock_permissions(lock_id: str, db: Session = Depends(get_db)):
    permissions = db.query(LockPermission).filter(LockPermission.lock_id == lock_id).all()
    return permissions


@router.get('/permissions/user/{user_id}', response_model=List[LockPermissionResponse])
def get_user_permissions(user_id: str, db: Session = Depends(get_db)):
    permissions = db.query(LockPermission).filter(LockPermission.user_id == user_id).all()
    return permissions


@router.post('/permissions', response_model=LockPermissionResponse, status_code=status.HTTP_201_CREATED)
def create_permission(permission: LockPermissionCreate, db: Session = Depends(get_db)):
    # Check if lock exists
    lock = db.query(Lock).filter(Lock.id == permission.lock_id).first()
    if lock is None:
        raise HTTPException(status_code=404, detail='Lock not found')
    
    # Check if user exists
    user = db.query(User).filter(User.id == permission.user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    
    # Check if permission already exists
    existing = db.query(LockPermission).filter(
        LockPermission.lock_id == permission.lock_id,
        LockPermission.user_id == permission.user_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail='Permission already exists')
    
    db_permission = LockPermission(
        id=str(uuid.uuid4()),
        lock_id=permission.lock_id,
        user_id=permission.user_id,
        can_unlock=permission.can_unlock,
        can_manage=permission.can_manage
    )
    
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission


@router.put('/permissions/{permission_id}', response_model=LockPermissionResponse)
def update_permission(permission_id: str, permission: LockPermissionUpdate, db: Session = Depends(get_db)):
    db_permission = db.query(LockPermission).filter(LockPermission.id == permission_id).first()
    if db_permission is None:
        raise HTTPException(status_code=404, detail='Permission not found')
    
    # Update only provided fields
    if permission.can_unlock is not None:
        db_permission.can_unlock = permission.can_unlock
    if permission.can_manage is not None:
        db_permission.can_manage = permission.can_manage
    
    db.commit()
    db.refresh(db_permission)
    return db_permission


@router.delete('/permissions/{permission_id}', response_model=LockPermissionResponse)
def delete_permission(permission_id: str, db: Session = Depends(get_db)):
    db_permission = db.query(LockPermission).filter(LockPermission.id == permission_id).first()
    if db_permission is None:
        raise HTTPException(status_code=404, detail='Permission not found')
    
    db.delete(db_permission)
    db.commit()
    return db_permission


# Lock access logs endpoints
@router.get('/logs', response_model=List[LockAccessLogResponse])
def get_all_logs(db: Session = Depends(get_db)):
    return db.query(LockAccessLog).all()


@router.get('/logs/lock/{lock_id}', response_model=List[LockAccessLogResponse])
def get_lock_logs(lock_id: str, db: Session = Depends(get_db)):
    logs = db.query(LockAccessLog).filter(LockAccessLog.lock_id == lock_id).all()
    return logs


@router.get('/logs/user/{user_id}', response_model=List[LockAccessLogResponse])
def get_user_logs(user_id: str, db: Session = Depends(get_db)):
    logs = db.query(LockAccessLog).filter(LockAccessLog.user_id == user_id).all()
    return logs