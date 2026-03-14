from pydantic import BaseModel, Field
from typing import Optional
from .enums import AIMode

class UserRequest(BaseModel):
    user_id: int = Field(..., example=1)
    message: str = Field(..., min_length=1, example="I was charged twice.")
    mode: AIMode = Field(default=AIMode.ASSISTED)
    session_id: Optional[str] = Field(None, description="Для відстеження історії чату")

class FeedbackRequest(BaseModel):
    case_id: str
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None