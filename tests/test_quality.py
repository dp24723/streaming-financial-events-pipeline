from finance_pipeline.quality import validate_jsonl


def test_validate_jsonl_splits_clean_and_bad_rows(tmp_path):
    path = tmp_path / "events.jsonl"
    path.write_text(
        '{"event_id":"1","event_time":"2026-01-01T00:00:00Z","account_id":"A1","symbol":"AAPL","side":"BUY","quantity":10,"price":100,"currency":"USD"}\n'
        '{"event_id":"bad","quantity":0}\n',
        encoding="utf-8",
    )

    result = validate_jsonl(path)

    assert len(result.clean) == 1
    assert len(result.rejected) == 1
