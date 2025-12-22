"""
Tests for LessonScraper domain class
"""
import pytest
from unittest.mock import Mock, call

from app.domains.lesson_data.interfaces import Child, Task
from app.domains.lesson_data.scraper import LessonScraper


class TestLessonScraper:
    """Tests for LessonScraper class"""

    def test_login_calls_http_client(self, lesson_scraper, mock_http_client):
        """Test that login method calls HTTP client with correct parameters"""
        # Arrange
        username = "test_user"
        password = "test_pass"

        # Act
        lesson_scraper._login(username, password)

        # Assert
        mock_http_client.request.assert_called_once()
        call_args = mock_http_client.request.call_args
        assert "admin/auth.htm" in call_args[0][0]
        assert call_args[1]["post_data"]["username"] == username
        assert call_args[1]["post_data"]["password"] == password

    def test_fetch_lesson_success(self, lesson_scraper, mock_http_client, mock_parser, sample_child):
        """Test successful lesson fetching"""
        # Arrange
        mock_parser.parse_children.return_value = [sample_child]
        mock_parser.parse_tasks.return_value = []
        mock_http_client.request.return_value = "<html>lesson</html>"

        # Act
        result = lesson_scraper.fetch_lesson("user", "pass", 123)

        # Assert
        assert len(result) == 1
        assert result[0].name == sample_child.name
        mock_parser.parse_children.assert_called_once()

    def test_get_child_tasks_fetches_task_texts(self, lesson_scraper, mock_http_client, mock_parser):
        """Test that task texts are fetched for each task"""
        # Arrange
        child = Child(
            name="Test",
            child_id=1,
            lesson_id="1",
            arepid=1,
            done_tasks_count=2,
            tasks=[],
        )
        tasks = [
            Task(id=1, name="Task 1", direction="Test", level="Easy", reward=10, text=None),
            Task(id=2, name="Task 2", direction="Test", level="Easy", reward=10, text=None),
        ]
        mock_parser.parse_tasks.return_value = tasks
        mock_parser.parse_task_text.return_value = "Task text"

        # Act
        result = lesson_scraper._get_child_tasks(child)

        # Assert
        assert len(result) == 2
        assert result[0].text == "Task text"
        assert result[1].text == "Task text"
        assert mock_parser.parse_task_text.call_count == 2



