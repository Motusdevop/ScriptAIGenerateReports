from typing import Any

from app.core.logger_config import logger
from app.domains.report_generation.gemini_client import GeminiClient
from app.domains.report_generation.prompt_builder import PromptBuilder


class ReportGenerator:

    @staticmethod
    async def generate_single_report(
        llm_client: GeminiClient, child: dict[str, Any]
    ) -> str:
        """Генерирует отчёт для одного ребёнка."""
        prompt = PromptBuilder.generate_prompt(child)

        try:
            llm_answer = await llm_client.call_llm(prompt)
        except Exception as exc:
            logger.exception(
                "Не удалось получить отчёт для {}: {}",
                child.get("name"),
                exc,
            )
            return "Не удалось получить отчёт. Попробуйте позже."

        sanitized_answer = " ".join(llm_answer.split())
        return sanitized_answer or "Нет данных для отчёта."
