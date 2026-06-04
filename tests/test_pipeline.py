from finance_pipeline.generator import generate_events
from finance_pipeline.pipeline import run_local_pipeline
from finance_pipeline.warehouse import read_table_counts


def test_pipeline_writes_warehouse_tables(tmp_path):
    raw = tmp_path / "raw" / "events.jsonl"
    db = tmp_path / "warehouse" / "finance.db"

    generate_events(rows=25, out_path=raw, seed=1)
    result = run_local_pipeline(raw, db)
    counts = read_table_counts(db)

    assert result["clean_events"] == 25
    assert counts["clean_events"] == 25
    assert counts["daily_metrics"] >= 1
