"""Tests for the FFXIV gil savings tracker."""

import csv
import os
from decimal import Decimal

from gilgoal.cli import main
from gilgoal.csv_export import export_csv
from gilgoal.goal import GoalProgress, can_afford
from gilgoal.storage import SaveData, Storage


def _tmp_path(name: str) -> str:
    return os.path.join(os.path.dirname(__file__), name)


def test_progress_no_goal() -> None:
    progress = GoalProgress.compute(0.0, 1000.0, 200.0)
    assert progress.balance == 800.0
    assert progress.remaining == 0.0
    assert progress.percent_complete == 100.0
    assert progress.is_complete is True


def test_progress_halfway() -> None:
    progress = GoalProgress.compute(10000.0, 6000.0, 1000.0)
    assert progress.balance == 5000.0
    assert progress.remaining == 5000.0
    assert progress.percent_complete == 50.0
    assert progress.is_complete is False


def test_progress_over_goal_caps_at_100() -> None:
    progress = GoalProgress.compute(5000.0, 9000.0, 1000.0)
    assert progress.balance == 8000.0
    assert progress.remaining == 0.0
    assert progress.percent_complete == 100.0
    assert progress.is_complete is True


def test_progress_overspend_clamps_percent_to_zero() -> None:
    progress = GoalProgress.compute(10000.0, 1000.0, 3000.0)
    assert progress.balance == -2000.0
    assert progress.remaining == 12000.0
    assert progress.percent_complete == 0.0
    assert progress.is_complete is False


def test_can_afford() -> None:
    assert can_afford(5000.0, 5000.0) is True
    assert can_afford(5000.0, 5001.0) is False
    assert can_afford(0.0, 0.0) is True
    assert can_afford(-100.0, 1.0) is False


def test_storage_round_trip(tmp_path) -> None:
    path = tmp_path / "test_data.json"
    storage = Storage(path)
    data = SaveData(goal_amount=5000.0)
    storage.add_transaction(data, "earn", 3000.0, "daily")
    storage.add_transaction(data, "spend", 500.0, "teleport")
    storage.save(data)

    loaded = storage.load()
    assert loaded.goal_amount == 5000.0
    assert len(loaded.transactions) == 2
    assert loaded.transactions[0].type == "earn"
    assert loaded.transactions[0].amount == 3000.0
    assert loaded.transactions[0].note == "daily"
    assert loaded.transactions[1].type == "spend"
    assert loaded.transactions[1].amount == 500.0


def test_storage_missing_file_returns_empty() -> None:
    storage = Storage("/nonexistent/path/data.json")
    data = storage.load()
    assert data.goal_amount == 0.0
    assert data.transactions == []


def test_storage_atomic_write_leaves_no_tmp(tmp_path) -> None:
    path = tmp_path / "test_data.json"
    storage = Storage(path)
    storage.save(SaveData(goal_amount=100.0))
    assert not path.with_name(path.name + ".tmp").exists()


def test_csv_export(tmp_path) -> None:
    data = SaveData(goal_amount=10000.0)
    data.transactions.append(
        type("Tx", (), {"timestamp": "2026-10-28T12:00:00", "type": "earn", "amount": 150000.0, "note": "roulette"})()
    )
    data.transactions.append(
        type("Tx", (), {"timestamp": "2026-10-28T12:01:00", "type": "spend", "amount": 42000.0, "note": "glamour"})()
    )

    out = tmp_path / "log.csv"
    export_csv(data, out)

    with out.open("r", newline="", encoding="utf-8") as f:
        reader = list(csv.reader(f))
    assert reader[0] == ["timestamp", "type", "amount", "note"]
    assert reader[1] == ["2026-10-28T12:00:00", "earn", "150000.00", "roulette"]
    assert reader[2] == ["2026-10-28T12:01:00", "spend", "42000.00", "glamour"]


def test_cli_status(tmp_path, capsys) -> None:
    path = tmp_path / "data.json"
    data = SaveData(goal_amount=1000000.0)
    data.transactions.append(
        type("Tx", (), {"timestamp": "2026-10-28T12:00:00", "type": "earn", "amount": 150000.0, "note": ""})()
    )
    data.transactions.append(
        type("Tx", (), {"timestamp": "2026-10-28T12:01:00", "type": "spend", "amount": 42000.0, "note": ""})()
    )
    Storage(path).save(data)

    code = main(["status", "--data", str(path)])
    assert code == 0
    captured = capsys.readouterr().out
    assert "1,000,000.00" in captured
    assert "150,000.00" in captured
    assert "42,000.00" in captured
    assert "108,000.00" in captured
    assert "10.8%" in captured


def test_parse_amount_handles_commas() -> None:
    from gilgoal.cli import parse_amount

    assert parse_amount("1000000") == 1000000.0
    assert parse_amount("1,000,000") == 1000000.0
    assert parse_amount("42.50") == 42.50
