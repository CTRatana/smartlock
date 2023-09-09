from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class HistoryListResponse(BaseModel):
    date: datetime
    user_id: int
