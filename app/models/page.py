from pydantic import BaseModel, Field
from typing import  List, Optional 
from datetime import datetime

class Page(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    linkedin_id: str
    name: str
    linkedin_url: str
    industry: Optional[str] = None
    followers_count: int | None = None
    head_count: Optional[int] = None
    specialities: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True