from uuid import UUID

from pydantic import BaseModel
from app.domains.lesson_data.schemas import Child


class ReportRequest(Child):
    pass


class ReportResponse(BaseModel):
    status: str
    report_id: UUID

    child_id: int
    child_name: str

    report: str
