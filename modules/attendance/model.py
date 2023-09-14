import datetime
from pydantic import BaseModel

class AttendanceInsertRequest(BaseModel):
    user_id: str
    date: datetime.datetime
