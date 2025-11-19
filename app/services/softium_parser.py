# services/softium_parser.py

from bs4 import BeautifulSoup
import re
from typing import List
from loguru import logger
from app.models.softium import Child, Task


class Parser:
    """Парсер HTML страниц Softium."""

    # -------------------------------------------------------------------------
    # CHILDREN PARSER
    # -------------------------------------------------------------------------
    @staticmethod
    def parse_children(lesson_html: str) -> List[Child]:
        """
        Парсит таблицы с детьми на странице урока.
        Возвращает список объектов Child.
        """
        logger.debug("🔍 Parsing children list...")
        soup = BeautifulSoup(lesson_html, "html.parser")
        children: List[Child] = []

        for table in soup.find_all("table", id=re.compile(r"reptable\d+")):
            try:
                name_td = table.find("td", text="Имя")
                done_td = table.find("td", text="Сделано заданий")
                if not name_td or not done_td:
                    continue

                # ссылки и атрибуты
                child_link = name_td.find_next_sibling("td").find("a")
                tasks_link = done_td.find_next_sibling("td").find("a", onclick=True)
                if not child_link or not tasks_link:
                    continue

                child_match = re.search(r"child=(\d+)", child_link["href"])
                task_match = re.search(
                    r"ShowTasks\((\d+),\s*'(.+?)',\s*(\d+),\s*(\d+)\)",
                    tasks_link["onclick"],
                )
                if not child_match or not task_match:
                    continue

                child = Child(
                    name=child_link.text.strip(),
                    child_id=int(child_match.group(1)),
                    lesson_id=task_match.group(2),
                    arepid=int(task_match.group(4)),
                    done_tasks_count=int(tasks_link.text.strip()),
                )
                children.append(child)

            except Exception as e:
                logger.error(f"❌ Error while parsing child row: {e}")

        logger.debug(f"👧 Parsed {len(children)} children")
        return children

    # -------------------------------------------------------------------------
    # TASKS PARSER
    # -------------------------------------------------------------------------
    @staticmethod
    def parse_tasks(tasks_html: str) -> List[Task]:
        """
        Парсит таблицу выполненных задач ребёнка.
        Возвращает список Task.
        """
        logger.debug("🔍 Parsing tasks...")
        soup = BeautifulSoup(tasks_html, "html.parser")
        table = soup.find("table", id="myTable")

        if not table or not table.tbody:
            logger.debug("⚠️ Tasks table not found")
            return []

        tasks: List[Task] = []

        for row in table.tbody.find_all("tr"):
            try:
                cells = row.find_all("td")
                if len(cells) < 5:
                    continue

                task = Task(
                    id_=int(cells[0].text.strip()),
                    name=cells[1].text.strip(),
                    direction=cells[2].text.strip(),
                    level=cells[3].text.strip(),
                    reward=int(cells[4].text.strip()),
                )
                tasks.append(task)

            except Exception as e:
                logger.error(f"❌ Error while parsing task row: {e}")

        logger.debug(f"📝 Parsed {len(tasks)} tasks")
        return tasks

    # -------------------------------------------------------------------------
    # TASK TEXT PARSER
    # -------------------------------------------------------------------------
    @staticmethod
    def parse_task_text(html_page: str) -> str:
        """
        Извлекает текст задания из textarea,
        очищает HTML и возвращает чистый текст.
        """
        logger.debug("🔍 Parsing task description...")
        soup = BeautifulSoup(html_page, "html.parser")

        textarea = soup.find("textarea", id="description")
        if not textarea:
            logger.debug("⚠️ Task textarea not found")
            return ""

        if not textarea.string:
            logger.debug("⚠️ Task textarea is empty")
            return ""

        try:
            inner_html = textarea.string
            inner_soup = BeautifulSoup(inner_html, "html.parser")

            paragraphs = inner_soup.find_all("p")
            text = "\n".join(p.get_text(strip=True) for p in paragraphs)

            logger.debug("📄 Task description parsed successfully")
            return text

        except Exception as e:
            logger.error(f"❌ Error parsing task description: {e}")
            return ""
