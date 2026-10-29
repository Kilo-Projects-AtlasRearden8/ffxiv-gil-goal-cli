"""Command line interface for the FFXIV gil savings goal tracker."""

from __future__ import annotations

import argparse
from decimal import Decimal, InvalidOperation

from .csv_export import export_csv
from .goal import GoalProgress, can_afford
from .storage import SaveData, Storage

DEFAULT_PATH = "gil_data.json"


def parse_amount(text: str) -> float:
    try:
        return float(Decimal(text.replace(",", "")))
    except (InvalidOperation, ValueError) as exc:
        raise argparse.ArgumentTypeError(f"invalid amount: {text}") from exc


def _totals(data: SaveData) -> tuple[float, float]:
    earned = sum(t.amount for t in data.transactions if t.type == "earn")
    spent = sum(t.amount for t in data.transactions if t.type == "spend")
    return earned, spent


def cmd_init(args, storage: Storage) -> int:
    if storage.path.exists():
        print(f"Data file already exists: {storage.path}")
        return 1
    storage.save(SaveData())
    print(f"Initialized data file: {storage.path}")
    return 0


def cmd_set_goal(args, storage: Storage) -> int:
    data = storage.load()
    data.goal_amount = args.amount
    storage.save(data)
    print(f"Savings goal set: {args.amount:,.2f} gil")
    return 0


def cmd_earn(args, storage: Storage) -> int:
    data = storage.load()
    storage.add_transaction(data, "earn", args.amount, args.note)
    storage.save(data)
    print(f"Logged +{args.amount:,.2f} gil earnings{f' ({args.note})' if args.note else ''}")
    return 0


def cmd_spend(args, storage: Storage) -> int:
    data = storage.load()
    storage.add_transaction(data, "spend", args.amount, args.note)
    storage.save(data)
    print(f"Logged -{args.amount:,.2f} gil spending{f' ({args.note})' if args.note else ''}")
    return 0


def cmd_status(args, storage: Storage) -> int:
    data = storage.load()
    earned, spent = _totals(data)
    progress = GoalProgress.compute(data.goal_amount, earned, spent)
    print(f"Goal:       {progress.goal_amount:,.2f} gil")
    print(f"Earned:     {progress.total_earned:,.2f} gil")
    print(f"Spent:      {progress.total_spent:,.2f} gil")
    print(f"Balance:    {progress.balance:,.2f} gil")
    print(f"Remaining:  {progress.remaining:,.2f} gil")
    print(f"Progress:   {progress.percent_complete:.1f}%")
    if progress.is_complete:
        print("Goal reached! Congratulations.")
    return 0


def cmd_afford(args, storage: Storage) -> int:
    data = storage.load()
    earned, spent = _totals(data)
    ok = can_afford(earned - spent, args.amount)
    print(f"Balance: {earned - spent:,.2f} gil")
    if ok:
        print(f"You can afford {args.amount:,.2f} gil.")
    else:
        print(f"You cannot afford {args.amount:,.2f} gil.")
    return 0


def cmd_export(args, storage: Storage) -> int:
    data = storage.load()
    export_csv(data, args.path)
    print(f"Exported {len(data.transactions)} transactions to {args.path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="gilgoal",
        description="Track FFXIV gil savings goals locally with JSON storage and CSV export.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    def add_path(parser_obj: argparse.ArgumentParser) -> argparse.ArgumentParser:
        parser_obj.add_argument("--path", default=DEFAULT_PATH, help="JSON data file path (default: gil_data.json)")
        return parser_obj

    p_init = add_path(sub.add_parser("init", help="create a new empty data file"))
    p_init.set_defaults(func=cmd_init)

    p_goal = add_path(sub.add_parser("set-goal", help="set the savings goal amount"))
    p_goal.add_argument("amount", type=parse_amount, help="goal amount in gil")
    p_goal.set_defaults(func=cmd_set_goal)

    p_earn = add_path(sub.add_parser("earn", help="log gil earnings"))
    p_earn.add_argument("amount", type=parse_amount, help="amount earned in gil")
    p_earn.add_argument("note", nargs="?", default="", help="optional note")
    p_earn.set_defaults(func=cmd_earn)

    p_spend = add_path(sub.add_parser("spend", help="log gil spending"))
    p_spend.add_argument("amount", type=parse_amount, help="amount spent in gil")
    p_spend.add_argument("note", nargs="?", default="", help="optional note")
    p_spend.set_defaults(func=cmd_spend)

    p_status = add_path(sub.add_parser("status", help="show progress toward the goal"))
    p_status.set_defaults(func=cmd_status)

    p_afford = add_path(sub.add_parser("afford", help="check if current balance covers a purchase"))
    p_afford.add_argument("amount", type=parse_amount, help="purchase cost in gil")
    p_afford.set_defaults(func=cmd_afford)

    p_export = sub.add_parser("export", help="export transactions to CSV")
    p_export.add_argument("path", help="output CSV file path")
    p_export.add_argument("--data", default=DEFAULT_PATH, help="JSON data file path (default: gil_data.json)")
    p_export.set_defaults(func=cmd_export)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    path = getattr(args, "data", None) or getattr(args, "path", None) or DEFAULT_PATH
    storage = Storage(path)
    return args.func(args, storage)


if __name__ == "__main__":
    raise SystemExit(main())
