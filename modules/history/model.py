import datetime
from pydantic import BaseModel, Field

class HistoryInsertRequest(BaseModel):
    user_id: str
    date: datetime.datetime
