import datetime
from pydantic import BaseModel

class HistoryInsertRequest(BaseModel):
    user_id: str
    # date: datetime.date
