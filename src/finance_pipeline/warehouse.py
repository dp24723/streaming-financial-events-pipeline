from collections import defaultdict
from pathlib import Path
import sqlite3

from finance_pipeline.schema import FinancialEvent


def _create_tables(conn: sqlite3.Connection) -> None:
    conn.execute("drop table if exists clean_events")
    conn.execute("drop table if exists daily_metrics")
    conn.execute(
        """
        create table clean_events (
            event_id text primary key,
            event_time text not null,
            event_date text not null,
            account_id text not null,
            symbol text not null,
            side text not null,
            quantity integer not null,
            price real not null,
            amount real not null,
            currency text not null
        )
        """
    )
    conn.execute(
        """
        create table daily_metrics (
            event_date text primary key,
            event_count integer not null,
            total_amount real not null,
            net_amount real not null,
            avg_price real not null,
            rejected_records integer not null
        )
        """
    )


def write_warehouse(db_path: Path, events: list[FinancialEvent], rejected_count: int) -> dict:
    if not events:
        raise ValueError("No clean events to write.")

    db_path.parent.mkdir(parents=True, exist_ok=True)
    daily: dict[str, dict] = defaultdict(lambda: {"count": 0, "total": 0.0, "net": 0.0, "price_sum": 0.0})

    with sqlite3.connect(db_path) as conn:
        _create_tables(conn)
        for event in events:
            amount = event.amount
            event_date = event.event_time.date().isoformat()
            conn.execute(
                """
                insert into clean_events values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event.event_id,
                    event.event_time.isoformat(),
                    event_date,
                    event.account_id,
                    event.symbol,
                    event.side,
                    event.quantity,
                    event.price,
                    amount,
                    event.currency,
                ),
            )
            daily[event_date]["count"] += 1
            daily[event_date]["total"] += abs(amount)
            daily[event_date]["net"] += amount
            daily[event_date]["price_sum"] += event.price

        last_date = sorted(daily)[-1]
        for event_date in sorted(daily):
            row = daily[event_date]
            conn.execute(
                "insert into daily_metrics values (?, ?, ?, ?, ?, ?)",
                (
                    event_date,
                    row["count"],
                    row["total"],
                    row["net"],
                    row["price_sum"] / row["count"],
                    rejected_count if event_date == last_date else 0,
                ),
            )
        conn.commit()

    return {"clean_events": len(events), "rejected_records": rejected_count, "db_path": str(db_path)}


def read_table_counts(db_path: Path) -> dict[str, int]:
    with sqlite3.connect(db_path) as conn:
        tables = ["clean_events", "daily_metrics"]
        return {table: conn.execute(f"select count(*) from {table}").fetchone()[0] for table in tables}
