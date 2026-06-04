from datetime import datetime, timedelta, timezone
from pathlib import Path
import json
import random
import uuid

SYMBOLS = ["AAPL", "MSFT", "NVDA", "AMZN", "GOOG", "TSLA", "JPM", "V"]


def generate_events(rows: int, out_path: Path, seed: int = 7) -> Path:
    random.seed(seed)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    start = datetime.now(timezone.utc) - timedelta(days=7)

    with out_path.open("w", encoding="utf-8") as f:
        for i in range(rows):
            event = {
                "event_id": str(uuid.uuid4()),
                "event_time": (start + timedelta(minutes=i * random.randint(1, 5))).isoformat(),
                "account_id": f"ACCT-{random.randint(1000, 9999)}",
                "symbol": random.choice(SYMBOLS),
                "side": random.choice(["BUY", "SELL"]),
                "quantity": random.randint(1, 500),
                "price": round(random.uniform(10, 750), 2),
                "currency": "USD",
            }
            f.write(json.dumps(event) + "\n")
    return out_path
