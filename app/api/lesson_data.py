from dataclasses import asdict

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_lesson_scraper, get_logger
from app.domains.lesson_data.schemas import Child, Children, LessonDataRequest
from app.domains.lesson_data.scraper import LessonScraper

router = APIRouter(prefix="/scraper", tags=["scraper"])


@router.post("/get_lesson_data")
def scrape(
    data: LessonDataRequest,
    logger=Depends(get_logger),
    scraper: LessonScraper = Depends(get_lesson_scraper),
) -> Children:
    logger.info("POST /scraper/get_lesson_data called")
    try:
        result = scraper.fetch_lesson(data.username, data.password, data.lesson_id)
    except Exception as exc:
        raise HTTPException(
            status_code=400, detail=f"Ошибка при получении данных: {exc}"
        )

    return Children(children=[Child(**asdict(c)) for c in result])
