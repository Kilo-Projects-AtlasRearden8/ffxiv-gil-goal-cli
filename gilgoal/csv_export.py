"""CSV export for gil goal transactions."""

from __future__ import annotations

import csv
from pathlib import Path

from .storage import SaveData


def export_csv(data: SaveData, path: str | Path) -> None:
    with Path(path).open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "type", "amount", "note"])
        for tx in data.transactions:
            writer.writerow([tx.timestamp, tx.type, f"{tx.amount:.2f}", tx.note])
