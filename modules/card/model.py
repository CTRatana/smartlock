from pydantic import BaseModel


class CardListResponse(BaseModel):
    id: int
    name: str


class CardInsertRequest(BaseModel):
    name: str


class CardUpdateRequest(BaseModel):
    name: str
