import time
import uuid

from fastapi import APIRouter, HTTPException, Request

from app.domains.report_generation.schemas import SingleLessonReportRequest
from app.domains.report_generation.generator import ReportGenerator
from app.domains.report_generation.gemini_client import GeminiClient
from app.core.config import settings
from app.core.logger_config import logger

router = APIRouter(prefix="/report_generation", tags=["report_generation"])


@router.post("/generate")
async def generate_report(payload: SingleLessonReportRequest, request: Request):
    """
    Генерирует отчёт для одного ребёнка.
    """
    t0 = time.perf_counter()
    req_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())

    child = payload.child.model_dump()
    child_id = child.get("child_id")
    child_name = child.get("name")

    progress = child.get("progress")  # если есть
    has_comment = bool((child.get("comments") or "").strip()) and child.get("comments") != "Нет комментариев."

    logger.info(
        "report_generation.start",
        extra={
            "req_id": req_id,
            "child_id": child_id,
            "child_name": child_name,
            "has_comment": has_comment,
            "progress": progress,
        },
    )

    try:
        llm_client = GeminiClient(
            model_name=settings.MODEL_NAME,
            api_key=settings.GEMINI_API_KEY,
        )

        report = await ReportGenerator.generate_single_report(llm_client, child)

        elapsed_ms = int((time.perf_counter() - t0) * 1000)
        logger.info(
            "report_generation.success",
            extra={
                "req_id": req_id,
                "child_id": child_id,
                "elapsed_ms": elapsed_ms,
                "report_len": len(report or ""),
            },
        )

        return {
            "status": "success",
            "child_id": child_id,
            "child_name": child_name,
            "report": report,
        }

    except Exception:
        elapsed_ms = int((time.perf_counter() - t0) * 1000)
        logger.exception(
            "report_generation.failed",
            extra={
                "req_id": req_id,
                "child_id": child_id,
                "child_name": child_name,
                "elapsed_ms": elapsed_ms,
            },
        )
        raise HTTPException(status_code=500, detail="Ошибка генерации отчёта")
