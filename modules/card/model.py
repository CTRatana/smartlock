from pydantic import BaseModel


class CardListResponse(BaseModel):
    id: int
    card_number: str


class CardInsertRequest(BaseModel):
    cacard_numberrd: str


class CardUpdateRequest(BaseModel):
    card_number: str
