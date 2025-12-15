import re
from typing import List
from lxml import html
from app.domains.lesson_data.interfaces import IParser, Child, Task


class LessonParser(IParser):
    """Парсер HTML страниц Softium (lxml-based)."""

    def __init__(self, logger) -> None:
        self.logger = logger

    def parse_children(self, lesson_html: str) -> List[Child]:
        self.logger.debug("🔍 Parsing children list (lxml)...")

        tree = html.fromstring(lesson_html)
        children: List[Child] = []

        tables = tree.xpath("//table[starts-with(@id, 'reptable')]")

        for table in tables:
            try:
                name_td = table.xpath(".//td[text()='Имя']")
                done_td = table.xpath(".//td[text()='Сделано заданий']")

                if not name_td or not done_td:
                    continue

                child_link = name_td[0].getnext().xpath(".//a")
                tasks_link = done_td[0].getnext().xpath(".//a[@onclick]")

                if not child_link or not tasks_link:
                    continue

                child_link = child_link[0]
                tasks_link = tasks_link[0]

                child_match = re.search(r"child=(\d+)", child_link.get("href", ""))
                task_match = re.search(
                    r"ShowTasks\((\d+),\s*'(.+?)',\s*(\d+),\s*(\d+)\)",
                    tasks_link.get("onclick", ""),
                )

                if not child_match or not task_match:
                    continue

                child = Child(
                    name=child_link.text_content().strip(),
                    child_id=int(child_match.group(1)),
                    lesson_id=task_match.group(2),
                    arepid=int(task_match.group(4)),
                    done_tasks_count=int(tasks_link.text_content().strip()),
                    tasks=[],
                )

                children.append(child)

            except Exception as e:
                self.logger.error(f"❌ Error while parsing child row: {e}")

        self.logger.debug(f"👧 Parsed {len(children)} children")
        return children

    def parse_tasks(self, tasks_html: str) -> List[Task]:
        self.logger.debug("🔍 Parsing tasks (lxml)...")

        tree = html.fromstring(tasks_html)
        rows = tree.xpath("//table[@id='myTable']/tbody/tr")

        tasks: List[Task] = []

        for row in rows:
            try:
                cells = row.xpath("./td")
                if len(cells) < 5:
                    continue

                task = Task(
                    id=int(cells[0].text_content().strip()),
                    name=cells[1].text_content().strip(),
                    direction=cells[2].text_content().strip(),
                    level=cells[3].text_content().strip(),
                    reward=int(cells[4].text_content().strip()),
                    text=None,
                )

                tasks.append(task)

            except Exception as e:
                self.logger.error(f"❌ Error while parsing task row: {e}")

        self.logger.debug(f"📝 Parsed {len(tasks)} tasks")
        return tasks

    def parse_task_text(self, html_page: str) -> str:
        self.logger.debug("🔍 Parsing task description (lxml)...")

        tree = html.fromstring(html_page)
        textarea = tree.xpath("//textarea[@id='description']")

        if not textarea or not textarea[0].text:
            self.logger.debug("⚠️ Task textarea not found or empty")
            return ""

        try:
            inner_tree = html.fromstring(textarea[0].text)
            paragraphs = inner_tree.xpath("//p")

            text = "\n".join(p.text_content().strip() for p in paragraphs)
            self.logger.debug("📄 Task description parsed successfully")
            return text

        except Exception as e:
            self.logger.error(f"❌ Error parsing task description: {e}")
            return ""
