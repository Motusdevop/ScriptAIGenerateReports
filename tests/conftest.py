"""
Pytest configuration and shared fixtures
"""
import pytest
from unittest.mock import Mock, AsyncMock
from fastapi.testclient import TestClient
from typing import Generator

from app.main import app
from app.domains.lesson_data.interfaces import IHttpClient, IParser, ILessonScraper
from app.domains.report_generation.interfaces import ILLMClient
from app.domains.lesson_data.scraper import LessonScraper
from app.domains.report_generation.generator import ReportGenerator
from app.core.logger_config import logger


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """FastAPI test client"""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def mock_logger():
    """Mock logger"""
    return logger


@pytest.fixture
def mock_http_client() -> IHttpClient:
    """Mock HTTP client"""
    mock = Mock(spec=IHttpClient)
    mock.request = Mock(return_value="<html>test</html>")
    return mock


@pytest.fixture
def mock_parser() -> IParser:
    """Mock parser"""
    mock = Mock(spec=IParser)
    mock.parse_children = Mock(return_value=[])
    mock.parse_tasks = Mock(return_value=[])
    mock.parse_task_text = Mock(return_value="Task text")
    return mock


@pytest.fixture
def mock_llm_client() -> ILLMClient:
    """Mock LLM client"""
    mock = AsyncMock(spec=ILLMClient)
    mock.generate = AsyncMock(return_value="Generated report text")
    return mock


@pytest.fixture
def lesson_scraper(mock_http_client, mock_parser, mock_logger) -> LessonScraper:
    """Lesson scraper instance with mocked dependencies"""
    return LessonScraper(
        http_client=mock_http_client,
        parser=mock_parser,
        base_url="https://test.com",
        logger=mock_logger,
    )


@pytest.fixture
def report_generator(mock_llm_client, mock_logger) -> ReportGenerator:
    """Report generator instance with mocked dependencies"""
    return ReportGenerator(llm_client=mock_llm_client, logger=mock_logger)


@pytest.fixture
def sample_child():
    """Sample child data for testing"""
    from app.domains.lesson_data.interfaces import Child, Task
    return Child(
        name="Тестовый Ребёнок",
        child_id=123,
        lesson_id="456",
        arepid=789,
        done_tasks_count=5,
        tasks=[
            Task(
                id=1,
                name="Задание 1",
                direction="Программирование",
                level="Средний",
                reward=10,
                text="Описание задания",
            )
        ],
    )

