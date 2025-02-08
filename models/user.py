from typing import Annotated, List, Optional
from pydantic import BaseModel, BeforeValidator, ConfigDict, Field
from datetime import date, datetime, time, timedelta

PyObjectId = Annotated[str, BeforeValidator(str)] 

class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    username: str = Field(...)
    assigned_movie: Optional[str] = Field(default = "")
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    time_taken: Optional[float] = None
    emoji_string: Optional[str] = Field(default="")
    emoji_count: Optional[int] = Field(default=0)
    success: Optional[bool] = None

class UpdateUser(BaseModel):
    assigned_movie: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    time_taken: Optional[float] = None
    emoji_string: Optional[str] = None
    emoji_count: Optional[int] = None
    success: Optional[bool] = None


class UserScore(BaseModel):
    username: str = None
    time_taken: float = None
    emoji_count: int = None

class User_List(BaseModel):
    total_players: List[UserScore] 