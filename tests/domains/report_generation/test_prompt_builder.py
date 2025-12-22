"""
Tests for prompt_builder domain class
"""
import pytest

from app.domains.report_generation.prompt_builder import PromptBuilder


class TestPromptBuilder:
    """Tests for PromptBuilder class"""

    def test_build_prompt_with_valid_data(self):
        """Test prompt building with valid input data"""
        # Arrange
        data = {
            "name": "Тестовый Ребёнок",
            "progress": 5,
            "tasks_block": "Test tasks",
            "comments": "Test comments",
        }

        # Act
        # Add test implementation based on prompt_builder logic

        prompt = PromptBuilder.generate_prompt(data)

        # Assert
        assert isinstance(prompt, str)
        assert len(prompt) == 2438
        assert "Имя ребёнка: Тестовый Ребёнок" in prompt

    def test_build_tasks_block(self):
        """Test building tasks block"""
        # Arrange
        tasks = [
            {"name": "Задание 1", "direction": "Математика", "text": "Решить уравнения."},
            {"name": "Задание 2", "direction": "Русский язык", "text": "Написать сочинение."},
        ]

        # Act
        tasks_block = PromptBuilder.build_tasks_block(tasks)

        # Assert
        expected_block = (
            "- Задание «Задание 1» (направление: Математика, Решить уравнения.)\n"
            "- Задание «Задание 2» (направление: Русский язык, Написать сочинение.)"
        )
        assert tasks_block == expected_block

    def test_generate_prompt_no_comments(self):
        """Test prompt generation when there are no comments"""
        # Arrange
        data = {
            "name": "Тестовый Ребёнок",
            "progress": 3,
            "tasks_block": "Test tasks",
            "comments": "",
        }

        # Act
        prompt = PromptBuilder.generate_prompt(data)

        # Assert
        assert "Комментарий преподавателя: Нет комментариев." in prompt
