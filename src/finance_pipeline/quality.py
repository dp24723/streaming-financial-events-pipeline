from dataclasses import dataclass
import json
from pathlib import Path

from pydantic import ValidationError

from finance_pipeline.schema import FinancialEvent


@dataclass(frozen=True)
class QualityResult:
    clean: list[FinancialEvent]
    rejected: list[dict]


def validate_jsonl(path: Path) -> QualityResult:
    clean: list[FinancialEvent] = []
    rejected: list[dict] = []

    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            try:
                payload = json.loads(line)
                clean.append(FinancialEvent.model_validate(payload))
            except (json.JSONDecodeError, ValidationError) as exc:
                rejected.append({"line_no": line_no, "error": str(exc), "raw": line.strip()})

    return QualityResult(clean=clean, rejected=rejected)
