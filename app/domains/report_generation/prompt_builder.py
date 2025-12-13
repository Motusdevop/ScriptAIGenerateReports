from typing import Any

from app.core.config import settings


class PromptBuilder:

    @staticmethod
    def generate_prompt(child: dict[str, Any]) -> str:
        tasks_block = PromptBuilder.build_tasks_block(child.get("tasks", []))
        progress = child.get("done_tasks_count", len(child.get("tasks", [])))
        comments = child.get("comments", "")
        comments_block = (
            f"\n\nКомментарий преподавателя:\n{comments.strip()}"
            if comments
            else "\n\nКомментарий преподавателя: Нет комментариев."
        )

        return (
            f"{settings.PROMPT.strip()}\n\n"
            f"Имя ребёнка: {child.get('name', 'Неизвестно')}\n"
            f"Количество выполненных заданий: {progress}\n"
            f"Выполненные задания:\n{tasks_block}"
            f"{comments_block}"
        )

    @staticmethod
    def format_task(task: dict) -> str:
        """Преобразует одно задание в строку для промпта."""
        task_name = task.get('name', 'Без названия')
        direction = task.get('direction', 'Не указано')
        task_text = task.get('text') or 'Нет описания'
        
        return (
            f"- Задание «{task_name}» "
            f"(направление: {direction}, {task_text})"
        )

    @staticmethod
    def build_tasks_block(tasks: list[dict]) -> str:
        """Создаёт текстовый блок со списком заданий."""
        if not tasks:
            return "Нет описаний выполненных заданий."
        return "\n".join(PromptBuilder.format_task(task) for task in tasks)
