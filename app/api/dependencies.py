from fastapi import Depends

from app.core.config import settings
from app.domains.report_generation.gemini_client import GeminiClient
from app.domains.report_generation.generator import ReportGenerator
from app.domains.lesson_data.scraper import LessonScraper
from app.core.logger_config import logger
from app.domains.lesson_data.client import HTTPClient
from app.domains.lesson_data.parser import LessonParser
from app.domains.report_generation.interfaces import ILLMClient
from app.domains.feedback.repository import JsonlFeedbackRepository
from app.domains.feedback.service import FeedbackService


def get_logger():
    return logger


def get_llm_client() -> ILLMClient:
    return GeminiClient(
        api_key=settings.GEMINI_API_KEY,
        model_name=settings.MODEL_NAME,
    )


def get_report_generator(
    llm: ILLMClient = Depends(get_llm_client), logger=Depends(get_logger)
) -> ReportGenerator:
    return ReportGenerator(llm_client=llm, logger=logger)


def get_http_client(logger=Depends(get_logger)):
    return HTTPClient(logger=logger)


def get_parser(logger=Depends(get_logger)):
    return LessonParser(logger=logger)


def get_lesson_scraper(
    http_client=Depends(get_http_client), parser=Depends(get_parser)
):
    return LessonScraper(
        http_client=http_client,
        parser=parser,
        base_url=settings.BASE_URL,
        logger=logger,
    )


def get_feedback_service() -> FeedbackService:
    repo = JsonlFeedbackRepository()
    return FeedbackService(repo)
