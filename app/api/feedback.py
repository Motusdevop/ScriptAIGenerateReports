from fastapi import APIRouter, Depends
from uuid import UUID

from app.api.dependencies import get_feedback_service
from app.domains.feedback.schemas import Feedback
from app.domains.feedback.service import FeedbackService

router = APIRouter(prefix="/api/v1/feedback", tags=["feedback"])


@router.post("")
def submit_feedback(
    feedback: Feedback, service: FeedbackService = Depends(get_feedback_service)
):
    service.submit_feedback(feedback)
    return {"status": "ok"}


@router.get("/{report_id}")
def get_feedback(
    report_id: UUID, service: FeedbackService = Depends(get_feedback_service)
):
    return service.get_feedback_for_report(report_id)
