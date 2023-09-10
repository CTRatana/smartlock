from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class HistoryListResponse(BaseModel):
    date: datetime
    user_id: int

class HistoryInsertRequest(BaseModel):
    user_id: int
