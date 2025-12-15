from typing import List
from app.domains.lesson_data.interfaces import (
    ILessonScraper,
    IHttpClient,
    IParser,
    Child,
    Task,
)


class LessonScraper(ILessonScraper):
    """Infrastructure: Softium lesson scraper"""

    def __init__(
        self, http_client: IHttpClient, parser: IParser, base_url: str, logger
    ):
        self.client = http_client
        self.parser = parser
        self.base_url = base_url
        self.logger = logger
        self.cookie_file: str | None = None

    def _login(self, username, password) -> None:
        self.logger.info("🔐 Logging in Softium...")
        self.cookie_file = "/tmp/softium_cookies.txt"

        self.client.request(
            f"{self.base_url}/admin/auth.htm",
            post_data={
                "username": username,
                "password": password,
            },
            cookiejar=self.cookie_file,
        )

    def fetch_lesson(self, username: str, password: str, lesson_id: int) -> List[Child]:
        self.logger.info(f"📘 Fetching lesson {lesson_id}")

        self._login(username, password)

        lesson_html = self.client.request(
            f"{self.base_url}/admin/lesson.htm?id={lesson_id}",
            cookiejar=self.cookie_file,
        )

        children = self.parser.parse_children(lesson_html)
        self.logger.info(f"👧 Found {len(children)} children")

        for child in children:
            child.tasks = self._get_child_tasks(child)

        return children

    def _get_child_tasks(self, child: Child) -> List[Task]:
        self.logger.debug(f"📄 Fetching tasks for: {child.name}")

        url = f"{self.base_url}/admin/childtasksdone.htm?kind=0&cid={child.child_id}&lid={child.lesson_id}&rid={child.arepid}"

        html_page = self.client.request(url, cookiejar=self.cookie_file)
        tasks = self.parser.parse_tasks(html_page)

        self.logger.debug(f"  — {len(tasks)} tasks found")

        for task in tasks:
            task.text = self.get_task_text(task.id)

        return tasks

    def get_task_text(self, task_id: int) -> str:
        self.logger.debug(f"📝 Fetching task text #{task_id}")

        url = f"{self.base_url}/admin/ulessoncontents.htm?id={task_id}"
        html_page = self.client.request(url, cookiejar=self.cookie_file)

        return self.parser.parse_task_text(html_page)
