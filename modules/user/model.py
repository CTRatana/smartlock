from pydantic import BaseModel


class UserListResponse(BaseModel):
    id: int
    username: str
    email: str


class UserInsertRequest(BaseModel):
    username: str
    email: str

class UserUpdateRequest(BaseModel):
    name: str
