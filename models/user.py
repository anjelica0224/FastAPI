from pydantic import BaseModel
from datetime import date, datetime, time, timedelta

class User(BaseModel):
    name: str
    emojis_used: int = None
    assigned_movie: str
    start_time: datetime = None
    end_time: datetime = None
    time_taken: float = None
