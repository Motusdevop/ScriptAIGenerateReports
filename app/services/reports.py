import asyncio
from typing import Any

from google import generativeai as genai

from app.config import settings
from app.logger_config import logger

MODEL = "gemini-2.5-flash"


def configure_gemini(api_key: str) -> None:
    """Настраивает использование Gemini."""
    genai.configure(api_key=api_key)


def format_task(task: dict) -> str:
    """Преобразует одно задание в строку для промпта."""
    return (
        f"- Задание «{task['name']}» "
        f"(направление: {task['direction']}, {task['text']})"
    )


def build_tasks_block(tasks: list[dict]) -> str:
    """Создаёт текстовый блок со списком заданий."""
    if not tasks:
        return "Нет описаний выполненных заданий."
    return "\n".join(format_task(task) for task in tasks)


def generate_prompt(child: dict[str, Any]) -> str:
    """Формирует полный промпт для одного ребёнка."""
    tasks_block = build_tasks_block(child.get("tasks", []))
    progress = child.get("done_tasks_count", len(child.get("tasks", [])))

    return (
        f"{settings.PROMPT.strip()}\n\n"
        f"Имя ребёнка: {child.get('name', 'Неизвестно')}\n"
        f"Количество выполненных заданий: {progress}\n"
        f"Выполненные задания:\n{tasks_block}"
    )


async def call_llm(prompt: str) -> str:
    """Вызывает LLM для конкретного промпта."""
    model = genai.GenerativeModel(model_name=MODEL)

    def _generate_content() -> str:
        response = model.generate_content(prompt)
        return (response.text or "").strip()

    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _generate_content)

async def generate_single_report(child: dict[str, Any]) -> str:
    """Генерирует отчёт для одного ребёнка."""
    prompt = generate_prompt(child)

    try:
        llm_answer = await call_llm(prompt)
    except Exception as exc:  # pragma: no cover
        logger.exception(
            "Не удалось получить отчёт для {}: {}",
            child.get("name"),
            exc,
        )
        return "Не удалось получить отчёт. Попробуйте позже."

    sanitized_answer = " ".join(llm_answer.split())
    return sanitized_answer or "Нет данных для отчёта."
