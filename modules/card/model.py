from pydantic import BaseModel


class CardListResponse(BaseModel):
    id: int
    card_number: str
    user_id: int

class CardInsertRequest(BaseModel):
    card_number: str
    user_id: int

class CardUpdateRequest(BaseModel):
    card_number: str
