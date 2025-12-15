from fastapi import APIRouter, Depends, HTTPException, Request

from app.api.dependencies import get_logger, get_report_generator
from app.domains.report_generation.generator import ReportGenerator
from app.domains.report_generation.schemas import ReportRequest, ReportResponse

router = APIRouter(prefix="/report_generation", tags=["report_generation"])


@router.post("/generate")
async def generate_report(
    payload: ReportRequest,
    request: Request,
    logger=Depends(get_logger),
    report_generator: ReportGenerator = Depends(get_report_generator),
) -> ReportResponse:
    """
    Генерирует отчёт для одного ребёнка.
    """

    logger.info("POST /report_generation/generate called")
    logger.info(payload.__repr__())

    try:
        report = await report_generator.generate_single_report(payload.model_dump())
        return ReportResponse(
            status="success",
            child_id=payload.child_id,
            child_name=payload.name,
            report=report,
        )

    except Exception as exc:
        logger.exception(exc)
        raise HTTPException(status_code=500, detail="Ошибка генерации отчёта")
