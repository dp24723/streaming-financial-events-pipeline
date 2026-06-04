from pathlib import Path
import os
import sqlite3

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Financial Pipeline Dashboard", layout="wide")
st.title("Financial Events Dashboard")

db_path = Path(os.getenv("PIPELINE_DB_PATH", "data/warehouse/finance.db"))
if not db_path.exists():
    st.warning("Warehouse not found. Run the pipeline first.")
    st.code("financial-pipeline generate --rows 1000 --out data/raw/events.jsonl\nfinancial-pipeline run-local --input data/raw/events.jsonl --db data/warehouse/finance.db")
    st.stop()

with sqlite3.connect(db_path) as conn:
    metrics = pd.read_sql_query("select * from daily_metrics order by event_date", conn)
    events = pd.read_sql_query("select * from clean_events order by event_time desc limit 200", conn)

c1, c2, c3 = st.columns(3)
c1.metric("Clean events", f"{len(events):,}")
c2.metric("Total volume", f"${metrics['total_amount'].sum():,.0f}")
c3.metric("Rejected records", int(metrics["rejected_records"].sum()) if "rejected_records" in metrics else 0)

st.subheader("Daily volume")
st.line_chart(metrics.set_index("event_date")[["total_amount", "net_amount"]])

st.subheader("Recent clean events")
st.dataframe(events, use_container_width=True)
