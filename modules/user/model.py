from pydantic import BaseModel


class UserListResponse(BaseModel):
    id: str
    username: str
    email: str
    card_number:str


class UserInsertRequest(BaseModel):
    id: str
    username: str
    email: str
    card_number:str

class UserUpdateRequest(BaseModel):
    username: str
    card_number:str
