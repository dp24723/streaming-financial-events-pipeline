# Streaming Financial Events Pipeline

Local pipeline that generates financial events, validates records, writes SQLite warehouse tables, and exposes a small dashboard.

```bash
pip install -e .[dev]
financial-pipeline generate --rows 1000 --out data/raw/events.jsonl
financial-pipeline run-local --input data/raw/events.jsonl --db data/warehouse/finance.db
financial-pipeline inspect --db data/warehouse/finance.db
pip install -e .[ui]
streamlit run dashboard.py
```
