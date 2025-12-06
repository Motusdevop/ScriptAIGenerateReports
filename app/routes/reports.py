# api/reports.py

from fastapi import APIRouter, HTTPException
from app.schemas import SingleLessonReportRequest
from app.services.reports import configure_gemini, generate_single_report
from app.config import settings

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("/generate")
async def generate_report(payload: SingleLessonReportRequest):
    """
    Генерирует отчёт для одного ребёнка.
    """
    configure_gemini(api_key=settings.GEMINI_API_KEY)

    child = payload.child.model_dump()

    try:
        report = await generate_single_report(child)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Ошибка генерации отчёта") from exc

    return {
        "status": "success",
        "child_id": child.get("child_id"),
        "child_name": child.get("name"),
        "report": report,
    }
