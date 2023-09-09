from pydantic import BaseModel


class UserListResponse(BaseModel):
    id: int
    name: str
    email: str


class UserInsertRequest(BaseModel):
    name: str
    email: str

class UserUpdateRequest(BaseModel):
    name: str
