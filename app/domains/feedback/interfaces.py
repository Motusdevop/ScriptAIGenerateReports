from abc import ABC, abstractmethod
from app.domains.feedback.schemas import Feedback
from typing import Iterable
from uuid import UUID


class FeedbackRepository(ABC):

    @abstractmethod
    def save(self, feedback: Feedback) -> None: ...

    @abstractmethod
    def get_by_report_id(self, report_id: UUID) -> list[Feedback]: ...

    @abstractmethod
    def iter_all(self) -> Iterable[Feedback]: ...
