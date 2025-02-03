from pydantic import BaseModel
from datetime import date, datetime, time, timedelta

class User(BaseModel):
    name: str
    time_taken: float 
    emojis_used: int
    # timestamp: datetime = datetime.utcnow()
