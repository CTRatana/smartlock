from pydantic import BaseModel


class AttendanceListResponse(BaseModel):
    id: int
    user_id: int


class AttendanceInsertRequest(BaseModel):
    user_id: int
