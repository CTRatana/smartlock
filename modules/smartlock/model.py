from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class LockBase(BaseModel):
    name: str
    location: str


class LockCreate(LockBase):
    pass


class LockUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    status: Optional[bool] = None


class LockResponse(LockBase):
    id: str
    status: bool
    last_updated: datetime

    class Config:
        orm_mode = True


class LockPermissionBase(BaseModel):
    lock_id: str
    user_id: str
    can_unlock: bool = True
    can_manage: bool = False


class LockPermissionCreate(LockPermissionBase):
    pass


class LockPermissionUpdate(BaseModel):
    can_unlock: Optional[bool] = None
    can_manage: Optional[bool] = None


class LockPermissionResponse(LockPermissionBase):
    id: str

    class Config:
        orm_mode = True


class LockAccessLogBase(BaseModel):
    lock_id: str
    user_id: Optional[str] = None
    action: str


class LockAccessLogCreate(LockAccessLogBase):
    pass


class LockAccessLogResponse(LockAccessLogBase):
    id: str
    timestamp: datetime

    class Config:
        orm_mode = True


class LockStatusUpdate(BaseModel):
    status: bool  # True = unlocked, False = locked
    user_id: str