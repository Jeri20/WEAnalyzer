# backend/schemas.py
from pydantic import BaseModel

class WebsiteEntityCreate(BaseModel):
    name: str
    url: str
    description: str
    score: float

class WebsiteEntityResponse(WebsiteEntityCreate):
    id: int

    class Config:
        orm_mode = True
