from typing import Any

from app.domains.report_generation.interfaces import ILLMClient
from app.domains.report_generation.prompt_builder import PromptBuilder


class ReportGenerator:

    def __init__(self, llm_client: ILLMClient, logger) -> None:
        self.llm_client = llm_client
        self.logger = logger

    async def generate_single_report(self, child: dict[str, Any]) -> str:
        prompt = PromptBuilder.generate_prompt(child)

        try:
            llm_answer = await self.llm_client.generate(prompt)
        except Exception as exc:
            self.logger.exception(
                "Не удалось получить отчёт для {}: {}",
                child.get("name"),
                exc,
            )
            return "Не удалось получить отчёт. Попробуйте позже."

        sanitized_answer = " ".join(llm_answer.split())
        return sanitized_answer or "Нет данных для отчёта."
