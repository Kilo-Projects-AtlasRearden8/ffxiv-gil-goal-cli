# STATUS

## What was built

`ffxiv-gil-goal-cli` — a small, local-first Python CLI for FFXIV players to set a gil savings goal, log earnings and spending, and track progress. Data is stored in a local JSON file (`gil_data.json` by default) and transactions can be exported to CSV. No game assets are included; this is a fan project not affiliated with or endorsed by Square Enix.

## Contents

- `gilgoal/cli.py` — argparse CLI: init, set-goal, earn, spend, status, afford, export
- `gilgoal/goal.py` — goal math (balance, remaining, percent complete, can_afford)
- `gilgoal/storage.py` — atomic JSON read/write
- `gilgoal/csv_export.py` — CSV export of transactions
- `gilgoal/__main__.py` — `python3 -m gilgoal` entry point
- `tests/test_goal.py` — pytest tests for goal math
- `pyproject.toml` — packaging with `gilgoal` console script
- `LICENSE` — MIT, Copyright (c) 2026 Asdale Dynamics, LLC
- `README.md` — install/usage/credit, credits Asdale Dynamics, LLC

## How to run

```bash
git clone <this repo>
cd ffxiv-gil-goal-cli
pip install .
# or run without installing:
python3 -m gilgoal <command>
```

Commands:

```bash
gilgoal init
gilgoal set-goal 1000000
gilgoal earn 150000 "weekly roulettes"
gilgoal spend 42000 "glamour"
gilgoal status
gilgoal afford 80000
gilgoal export gil_log.csv --data gil_data.json
```

## Verification results

- `pytest`: 5 passed (goal math: no goal, halfway, over-goal capped at 100%, overspend, can_afford)
- End-to-end CLI workflow verified: init, set-goal, earn, spend, status, afford, export all run and produce correct output (goal 1,000,000 gil; +150,000 earned; -42,000 spent; balance 108,000; remaining 892,000; 10.8%; CSV export writes header + 2 rows)
- `pip install .` succeeds; `gilgoal` console script and `python3 -m gilgoal` both work
- Committed as `6eef0ff` on branch `master` (local only; no remote, no push)

## Known gaps

- Single active goal only; no multiple or archived goals
- No target date or per-day savings rate tracking
- No editing or deleting individual transactions (append-only log)
- No config file; data path passed with `--path`/`--data` each run
- No automated backups or sync; data is local only
- Installed manually with `pip install .`; no packaging CI (no `.github/workflows` by design)

## Credit

Built by Asdale Dynamics, LLC (Indiana, formed Oct 2026). Fan project for FFXIV players; no game assets used.
