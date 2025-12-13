from fastapi import APIRouter, HTTPException
from app.domains.lesson_data.scraper import LessonScraper

router = APIRouter(prefix="/scraper", tags=["scraper"])


@router.get("/get_lesson_data")
def scrape(username: str, password: str, lesson_id: int):
    scraper = LessonScraper(username=username, password=password)

    try:
        data = scraper.get_lesson_data(lesson_id)
    except Exception as exc:
        raise HTTPException(
            status_code=400, detail=f"Ошибка при получении данных: {exc}"
        )

    return {"children": [c.model_dump() for c in data]}
