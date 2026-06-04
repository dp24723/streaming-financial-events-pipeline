from pathlib import Path

from finance_pipeline.quality import validate_jsonl
from finance_pipeline.warehouse import write_warehouse


def run_local_pipeline(input_path: Path, db_path: Path) -> dict:
    quality = validate_jsonl(input_path)
    return write_warehouse(db_path, quality.clean, rejected_count=len(quality.rejected))
