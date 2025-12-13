from typing import List, Optional
from pydantic import BaseModel


class Task(BaseModel):

    id: int
    name: str
    direction: str
    level: str
    reward: int
    text: Optional[str] = None


class Child(BaseModel):

    name: str
    child_id: int
    lesson_id: str
    arepid: int
    done_tasks_count: int
    tasks: List[Task] = []
    comments: Optional[str] = None
