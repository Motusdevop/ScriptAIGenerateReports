from dataclasses import dataclass
from typing import Protocol, List, Optional


@dataclass
class Task:
    id: int
    name: str
    direction: str
    level: str
    reward: int
    text: Optional[str]


@dataclass
class Child:
    name: str
    child_id: int
    lesson_id: str
    arepid: int
    done_tasks_count: int
    tasks: List[Task]


class ILessonScraper(Protocol):
    def fetch_lesson(
        self, username: str, password: str, lesson_id: int
    ) -> List[Child]: ...


class IHttpClient(Protocol):
    def request(
        self,
        url: str,
        *,
        post_data: dict | None = None,
        cookiejar: str | None = None,
    ) -> str: ...


class IParser(Protocol):
    def parse_children(self, lesson_html: str) -> List[Child]: ...
    def parse_tasks(self, tasks_html: str) -> List[Task]: ...
    def parse_task_text(self, html_page: str) -> str: ...
