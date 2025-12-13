from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Page(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    linkedin_url: str
    industry: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True