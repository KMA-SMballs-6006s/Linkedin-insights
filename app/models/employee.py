from pydantic import BaseModel, Field
from typing import Optional

class Employee(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    page_id: str
    name: str
    title: Optional[str] = None
    location: Optional[str] = None

    class Config:
        populate_by_name = True