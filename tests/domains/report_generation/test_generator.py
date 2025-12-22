"""
Tests for ReportGenerator domain class
"""
import pytest
from unittest.mock import AsyncMock

from app.domains.report_generation.generator import ReportGenerator


class TestReportGenerator:
    """Tests for ReportGenerator class"""

    @pytest.mark.asyncio
    async def test_generate_single_report_success(self, report_generator, mock_llm_client):
        """Test successful report generation"""
        # Arrange
        mock_llm_client.generate.return_value = "Сгенерированный отчёт о работе ребёнка."
        payload = {
            "child_id": 123,
            "name": "Тестовый Ребёнок",
            "progress": 5,
            "tasks_block": "Test tasks",
            "comments": "Test comments",
        }

        # Act
        result = await report_generator.generate_single_report(payload)

        # Assert
        assert result == "Сгенерированный отчёт о работе ребёнка."
        mock_llm_client.generate.assert_called_once()
        assert "Тестовый Ребёнок" in mock_llm_client.generate.call_args[0][0]

    @pytest.mark.asyncio
    async def test_generate_single_report_handles_errors(self, report_generator, mock_llm_client):
        """Test error handling in report generation"""
        # Arrange
        mock_llm_client.generate.side_effect = Exception("LLM error")
        payload = {
            "child_id": 123,
            "name": "Тестовый Ребёнок",
            "progress": 5,
            "tasks_block": "Test tasks",
            "comments": "Test comments",
        }

        assert await report_generator.generate_single_report(payload) == "Не удалось получить отчёт. Попробуйте позже."

