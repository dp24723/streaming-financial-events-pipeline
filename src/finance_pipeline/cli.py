from pathlib import Path
import argparse
import json

from finance_pipeline.generator import generate_events
from finance_pipeline.pipeline import run_local_pipeline
from finance_pipeline.warehouse import read_table_counts


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="financial-pipeline")
    sub = parser.add_subparsers(dest="command", required=True)

    gen = sub.add_parser("generate")
    gen.add_argument("--rows", type=int, default=1000)
    gen.add_argument("--out", type=Path, default=Path("data/raw/events.jsonl"))
    gen.add_argument("--seed", type=int, default=7)

    run = sub.add_parser("run-local")
    run.add_argument("--input", type=Path, default=Path("data/raw/events.jsonl"))
    run.add_argument("--db", type=Path, default=Path("data/warehouse/finance.db"))

    inspect = sub.add_parser("inspect")
    inspect.add_argument("--db", type=Path, default=Path("data/warehouse/finance.db"))
    return parser


def main() -> None:
    args = build_parser().parse_args()

    if args.command == "generate":
        path = generate_events(args.rows, args.out, args.seed)
        print(f"Generated {args.rows} events at {path}")
        return

    if args.command == "run-local":
        result = run_local_pipeline(args.input, args.db)
        print(json.dumps(result, indent=2))
        return

    if args.command == "inspect":
        print(json.dumps(read_table_counts(args.db), indent=2))
