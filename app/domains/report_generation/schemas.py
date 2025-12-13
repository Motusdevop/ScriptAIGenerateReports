from typing import List

from pydantic import BaseModel
from app.domains.lesson_data.schemas import Child


class SingleLessonReportRequest(BaseModel):
    child: Child
