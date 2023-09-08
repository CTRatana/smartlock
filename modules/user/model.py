from pydantic import BaseModel


class SampleListResponse(BaseModel):
    id: int
    name: str


class SampleInsertRequest(BaseModel):
    name: str


class SampleUpdateRequest(BaseModel):
    name: str
