# """
# Tests for lesson_data API endpoints
# """
# import pytest
# from unittest.mock import Mock
# from fastapi.testclient import TestClient
#
# from app.main import app
# from app.api.dependencies import get_lesson_scraper
# from app.domains.lesson_data.schemas import LessonDataRequest
#
#
# @pytest.fixture
# def mock_scraper(sample_child):
#     """Mock lesson scraper"""
#     mock = Mock()
#     mock.fetch_lesson.return_value = [sample_child]
#     return mock
#
#
# class TestLessonDataEndpoint:
#     """Tests for /scraper/get_lesson_data endpoint"""
#
#     def test_get_lesson_data_success(self, client: TestClient, mock_scraper, sample_child):
#         """Test successful lesson data retrieval"""
#         # Arrange
#         app.dependency_overrides[get_lesson_scraper] = lambda: mock_scraper
#         request_data = LessonDataRequest(
#             username="test_user",
#             password="test_pass",
#             lesson_id=123,
#         )
#
#         try:
#             # Act
#             response = client.post("/scraper/get_lesson_data", json=request_data.model_dump())
#
#             # Assert
#             assert response.status_code == 200
#             data = response.json()
#             assert "children" in data
#             assert len(data["children"]) == 1
#             assert data["children"][0]["name"] == "Тестовый Ребёнок"
#         finally:
#             # Cleanup
#             app.dependency_overrides.clear()
#
#     def test_get_lesson_data_error(self, client: TestClient):
#         """Test error handling in lesson data endpoint"""
#         # Arrange
#         mock_scraper = Mock()
#         mock_scraper.fetch_lesson.side_effect = Exception("Test error")
#         app.dependency_overrides[get_lesson_scraper] = lambda: mock_scraper
#
#         request_data = LessonDataRequest(
#             username="test_user",
#             password="test_pass",
#             lesson_id=123,
#         )
#
#         try:
#             # Act
#             response = client.post("/scraper/get_lesson_data", json=request_data.model_dump())
#
#             # Assert
#             assert response.status_code == 400
#             assert "Ошибка при получении данных" in response.json()["detail"]
#         finally:
#             # Cleanup
#             app.dependency_overrides.clear()
#
