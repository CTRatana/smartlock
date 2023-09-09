from pydantic import BaseModel


class HistoryListResponse(BaseModel):
    id: int
    name: str


class HistoryInsertRequest(BaseModel):
    name: str


class HistoryUpdateRequest(BaseModel):
    name: str
