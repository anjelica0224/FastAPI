from pydantic import BaseModel
from typing import List, Optional

class Movie(BaseModel):
    title: str
    genres: Optional[List[str]]
    year: Optional[int]
