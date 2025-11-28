from fastapi import APIRouter, HTTPException

from app.schemas import LessonReportRequest
from app.services.reports import configure_gemini, collect_reports
from app.config import settings

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("/generate")
async def generate_report(payload: LessonReportRequest):
    """
    Генерирует отчет на основе переданных данных урока.
    """
    if not payload.children:
        raise HTTPException(status_code=400, detail="Нет данных для генерации отчёта")

    configure_gemini(api_key=settings.GEMINI_API_KEY)

    children = [child.model_dump() for child in payload.children]
    report = await collect_reports(children)

    return {"status": "success", "report": report}
