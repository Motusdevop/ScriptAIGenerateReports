from pydantic import BaseModel, Field
from typing import Optional, Literal
from uuid import UUID
from datetime import datetime

from app.domains.lesson_data.schemas import Child


class Feedback(BaseModel):
    report_id: UUID
    rating: Literal[1, -1]  # like / dislike
    comment: Optional[str] = None

    child: Child
    prompt: str
    response: str
    model: str = "gemini"

    created_at: datetime = Field(default_factory=datetime.now)
