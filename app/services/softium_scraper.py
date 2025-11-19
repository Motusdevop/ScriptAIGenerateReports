from loguru import logger
from typing import List
from app.services.softium_client import HTTPClient
from app.services.softium_parser import Parser
from app.models.softium import Child, Task

from app.config import settings


class LessonScraper:
    """Скрейпер уроков + детей + заданий + текста"""

    def __init__(self, username: str, password: str):
        self.client = HTTPClient()
        self.username = username
        self.password = password
        self.cookie_file: str = ""

    def login(self) -> None:
        """Логин и сохранение cookies"""
        logger.info("🔐 Logging in Softium...")
        self.cookie_file = "/tmp/softium_cookies.txt"

        self.client.request(
            f"{settings.BASE_URL}/admin/auth.htm",
            post_data={"username": self.username, "password": self.password},
            cookiejar=self.cookie_file,
        )

        logger.info("✅ Login successful")

    def get_lesson_data(self, lesson_id: int) -> List[Child]:
        logger.info(f"📘 Fetching lesson {lesson_id}")

        self.login()

        lesson_html = self.client.request(
            f"{settings.BASE_URL}/admin/lesson.htm?id={lesson_id}",
            cookiejar=self.cookie_file,
        )

        children = Parser.parse_children(lesson_html)
        logger.info(f"👧 Found {len(children)} children")

        for child in children:
            child.tasks = self.get_child_tasks(child)

        return children

    def get_child_tasks(self, child: Child) -> List[Task]:
        logger.debug(f"📄 Fetching tasks for: {child.name}")

        url = f"{settings.BASE_URL}/admin/childtasksdone.htm?kind=0&cid={child.child_id}&lid={child.lesson_id}&rid={child.arepid}"

        html_page = self.client.request(url, cookiejar=self.cookie_file)
        tasks = Parser.parse_tasks(html_page)

        logger.debug(f"  — {len(tasks)} tasks found")

        for task in tasks:
            task.text = self.get_task_text(task.id)

        return tasks

    def get_task_text(self, task_id: int) -> str:
        logger.debug(f"📝 Fetching task text #{task_id}")

        url = f"{settings.BASE_URL}/admin/ulessoncontents.htm?id={task_id}"
        html_page = self.client.request(url, cookiejar=self.cookie_file)

        return Parser.parse_task_text(html_page)
