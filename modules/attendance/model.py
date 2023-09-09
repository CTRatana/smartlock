from pydantic import BaseModel


class AttendanceListResponse(BaseModel):
    id: int
    name: str


class AttendanceInsertRequest(BaseModel):
    name: str


class AttendanceUpdateRequest(BaseModel):
    name: str
