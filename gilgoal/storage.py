"""Local JSON storage for gil goal data."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass
class Transaction:
    timestamp: str
    type: str
    amount: float
    note: str = ""


@dataclass
class SaveData:
    goal_amount: float = 0.0
    transactions: list[Transaction] = field(default_factory=list)


class Storage:
    def __init__(self, path: str | Path = "gil_data.json") -> None:
        self.path = Path(path)

    def load(self) -> SaveData:
        if not self.path.exists():
            return SaveData()
        try:
            with self.path.open("r", encoding="utf-8") as f:
                raw = json.load(f)
        except (json.JSONDecodeError, OSError):
            return SaveData()
        data = SaveData(goal_amount=float(raw.get("goal_amount", 0.0) or 0.0))
        for tx in raw.get("transactions", []):
            data.transactions.append(
                Transaction(
                    timestamp=str(tx.get("timestamp", "")),
                    type=str(tx.get("type", "")),
                    amount=float(tx.get("amount", 0.0) or 0.0),
                    note=str(tx.get("note", "")),
                )
            )
        return data

    def save(self, data: SaveData) -> None:
        payload = {
            "goal_amount": data.goal_amount,
            "transactions": [
                {
                    "timestamp": t.timestamp,
                    "type": t.type,
                    "amount": t.amount,
                    "note": t.note,
                }
                for t in data.transactions
            ],
        }
        tmp = self.path.with_name(self.path.name + ".tmp")
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        tmp.replace(self.path)

    def add_transaction(self, data: SaveData, tx_type: str, amount: float, note: str = "") -> SaveData:
        data.transactions.append(
            Transaction(
                timestamp=datetime.now().isoformat(timespec="seconds"),
                type=tx_type,
                amount=float(amount),
                note=note,
            )
        )
        return data
