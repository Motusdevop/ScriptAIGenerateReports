from __future__ import annotations

from pathlib import Path
import json
from datetime import datetime
from uuid import UUID
from typing import Iterable

from app.domains.feedback.interfaces import FeedbackRepository
from app.domains.feedback.schemas import Feedback


class JsonlFeedbackRepository(FeedbackRepository):

    def __init__(self, base_dir: str = "data/feedback"):
        self.base_path = Path(base_dir)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def _get_file_path(self) -> Path:
        filename = datetime.now().strftime("%Y-%m.jsonl")
        return self.base_path / filename

    def _to_json_line(self, feedback: Feedback) -> str:
        payload = feedback.model_dump(mode="json")  # UUID/datetime -> json-friendly
        return json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(", ", ": "),
        )

    def save(self, feedback: Feedback) -> None:
        path = self._get_file_path()
        new_line = self._to_json_line(feedback)
        report_id_str = str(feedback.report_id)

        lines: list[str] = []
        if path.exists():
            lines = path.read_text(encoding="utf-8").splitlines()

        found = False
        changed = False

        for i in range(len(lines)):
            raw = lines[i].strip()
            if not raw:
                continue

            try:
                obj = json.loads(raw)
            except json.JSONDecodeError:
                continue

            if str(obj.get("report_id")) != report_id_str:
                continue

            found = True

            old_rating = obj.get("rating")
            try:
                old_rating_int = int(old_rating)
            except Exception:
                old_rating_int = None

            if old_rating_int == feedback.rating:
                return

            lines[i] = new_line
            changed = True
            break

        if not found:
            lines.append(new_line)
            changed = True

        if changed:
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def get_by_report_id(self, report_id: UUID) -> list[Feedback]:
        results: list[Feedback] = []
        for fb in self.iter_all():
            if fb.report_id == report_id:
                results.append(fb)
        return results

    def iter_all(self) -> Iterable[Feedback]:
        for file in sorted(self.base_path.glob("*.jsonl")):
            with file.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        yield Feedback.model_validate_json(line)
                    except Exception:
                        continue
