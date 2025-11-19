from pydantic import BaseModel
from typing import List


class TaskModel(BaseModel):
    id: int
    name: str
    direction: str
    level: str
    reward: int
    text: str


class ChildModel(BaseModel):
    name: str
    child_id: int
    lesson_id: str
    arepid: int
    done_tasks_count: int
    tasks: List[TaskModel]


class LessonReportRequest(BaseModel):
    children: List[ChildModel]
