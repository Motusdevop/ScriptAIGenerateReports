"""
Tests for report_generation API endpoints
"""




# @pytest.fixture
# def mock_report_generator():
#     """Mock report generator"""
#     mock = Mock()
#     mock.generate_single_report = AsyncMock(return_value="Сгенерированный отчёт о работе ребёнка.")
#     return mock


# class TestReportGenerationEndpoint:
#     """Tests for /report_generation/generate endpoint"""
#
#     def test_generate_report_success(self, client: TestClient, mock_report_generator):
#         """Test successful report generation"""
#         # Arrange
#         app.dependency_overrides[get_report_generator] = lambda: mock_report_generator
#         request_data = ReportRequest(
#             child_id=123,
#             name="Тестовый Ребёнок",
#             progress=5,
#             tasks_block="Test tasks",
#             comments="Test comments",
#         )
#
#         try:
#             # Act
#             response = client.post(
#                 "/report_generation/generate",
#                 json=request_data.model_dump(),
#             )
#
#             # Assert
#             assert response.status_code == 200
#             data = response.json()
#             assert data["status"] == "success"
#             assert data["child_id"] == 123
#             assert data["child_name"] == "Тестовый Ребёнок"
#             assert "report" in data
#         finally:
#             # Cleanup
#             app.dependency_overrides.clear()
#
#     def test_generate_report_error(self, client: TestClient):
#         """Test error handling in report generation"""
#         # Arrange
#         mock_generator = Mock()
#         mock_generator.generate_single_report = AsyncMock(side_effect=Exception("Test error"))
#         app.dependency_overrides[get_report_generator] = lambda: mock_generator
#
#         request_data = ReportRequest(
#             child_id=123,
#             name="Тестовый Ребёнок",
#             progress=5,
#             tasks_block="Test tasks",
#             comments="Test comments",
#         )
#
#         try:
#             # Act
#             response = client.post(
#                 "/report_generation/generate",
#                 json=request_data.model_dump(),
#             )
#
#             # Assert
#             assert response.status_code == 500
#             assert "Ошибка генерации отчёта" in response.json()["detail"]
#         finally:
#             # Cleanup
#             app.dependency_overrides.clear()
