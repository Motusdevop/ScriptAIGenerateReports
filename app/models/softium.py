# models/softium.py

from typing import List, Optional


class Task:
    """Модель задания"""

    def __init__(
        self,
        id_: int,
        name: str,
        direction: str,
        level: str,
        reward: int,
        text: Optional[str] = None,
    ):
        self.id = id_
        self.name = name
        self.direction = direction
        self.level = level
        self.reward = reward
        self.text = text

    def to_dict(self):
        return self.__dict__


class Child:
    """Модель ребёнка"""

    def __init__(
        self,
        name: str,
        child_id: int,
        lesson_id: str,
        arepid: int,
        done_tasks_count: int,
    ):
        self.name = name
        self.child_id = child_id
        self.lesson_id = lesson_id
        self.arepid = arepid
        self.done_tasks_count = done_tasks_count
        self.tasks: List[Task] = []

    def to_dict(self):
        return {**self.__dict__, "tasks": [task.to_dict() for task in self.tasks]}
