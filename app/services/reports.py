from google import generativeai as genai

from app.config import settings

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
    return "\n".join(format_task(task) for task in tasks)


def make_prompt_for_children(children: list[dict]) -> str:
    """Создаёт текстовый промпт для отчёта по одному ребёнку."""

    prompt = settings.PROMPT

    for i, child in enumerate(children, start=1):
        tasks_block = build_tasks_block(child["tasks"])

        prompt += f"""
Вот данные о ребёнке {i}:
Имя: {child['name']}
Выполненные задания:
{tasks_block}"""

    return prompt


def send_to_gemini(prompt: str) -> str:
    """Отправляет промпт в Gemini и возвращает текст ответа."""
    model = genai.GenerativeModel(model_name=MODEL)
    response = model.generate_content(prompt)
    return response.text.strip()
