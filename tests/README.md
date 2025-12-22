# Тесты проекта

## Структура тестов

```
tests/
├── __init__.py
├── conftest.py                 # Общие фикстуры и конфигурация pytest
├── requirements.txt            # Зависимости для тестирования
├── README.md                   # Этот файл
│
├── api/                        # Тесты API endpoints
│   ├── __init__.py
│   ├── test_lesson_data.py    # Тесты /scraper/get_lesson_data
│   └── test_report_generation.py  # Тесты /report_generation/generate
│
├── domains/                    # Тесты domain слоя
│   ├── __init__.py
│   │
│   ├── lesson_data/           # Тесты lesson_data domain
│   │   ├── __init__.py
│   │   ├── test_scraper.py    # Тесты LessonScraper
│   │   ├── test_client.py     # Тесты HTTPClient
│   │   └── test_parser.py     # Тесты LessonParser
│   │
│   └── report_generation/     # Тесты report_generation domain
│       ├── __init__.py
│       ├── test_generator.py  # Тесты ReportGenerator
│       ├── test_gemini_client.py  # Тесты GeminiClient
│       └── test_prompt_builder.py # Тесты PromptBuilder
│
└── integration/               # Интеграционные тесты
    ├── __init__.py
    └── test_api_flow.py       # Полные сценарии использования API
```

## Запуск тестов

```bash
# Установить зависимости для тестов
pip install -r tests/requirements.txt

# Запустить все тесты
pytest

# Запустить тесты с покрытием
pytest --cov=app --cov-report=html

# Запустить только unit тесты
pytest tests/api tests/domains

# Запустить только интеграционные тесты
pytest tests/integration -m integration

# Запустить тесты конкретного модуля
pytest tests/api/test_lesson_data.py

# Запустить тесты в verbose режиме
pytest -v
```

## Принципы организации

1. **Зеркальная структура**: Структура `tests/` зеркалирует структуру `app/`
2. **Фикстуры**: Общие фикстуры в `conftest.py`
3. **Моки**: Используются моки для внешних зависимостей (HTTP, LLM API)
4. **Изоляция**: Каждый тест независим и использует моки вместо реальных сервисов
5. **Async тесты**: Для async функций используется `@pytest.mark.asyncio`

## Заполнение тестов

Большинство тестовых функций содержат заглушки (`pass`). Необходимо заполнить их реальной логикой тестирования на основе реализации классов.

