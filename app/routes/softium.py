from fastapi import APIRouter
from app.services.softium_scraper import LessonScraper

router = APIRouter(prefix="/scraper", tags=["scraper"])


@router.get("/get_lesson_data")
def scrape(username: str, password: str, lesson_id: int):
    scraper = LessonScraper(username=username, password=password)

    data = scraper.get_lesson_data(lesson_id)
    return {"children": [c.to_dict() for c in data]}
