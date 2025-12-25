from uuid import UUID

from app.domains.feedback.schemas import Feedback
from app.domains.feedback.interfaces import FeedbackRepository


class FeedbackService:

    def __init__(self, repository: FeedbackRepository):
        self._repository = repository

    def submit_feedback(self, feedback: Feedback) -> None:
        self._repository.save(feedback)

    def get_feedback_for_report(self, report_id: UUID) -> list[Feedback]:
        return self._repository.get_by_report_id(report_id)
