# ffxiv-gil-goal-cli

A small Python CLI for FFXIV players to set a gil savings goal, log earnings and spending, and track progress. Data lives in a local JSON file, and transactions can be exported to CSV.

Built by **Asdale Dynamics, LLC** — a fan project for FFXIV players. No game assets are included, and this tool is not affiliated with or endorsed by Square Enix.

## Install

```bash
git clone https://github.com/dylanasdale/ffxiv-gil-goal-cli.git
cd ffxiv-gil-goal-cli
pip install .
```

Or run straight from the folder:

```bash
python3 -m gilgoal.cli ...
```

## Usage

Initialize a data file:

```bash
gilgoal init
```

Set a savings goal:

```bash
gilgoal set-goal 1000000
```

Log earnings and spending:

```bash
gilgoal earn 150000 "weekly roulettes"
gilgoal spend 42000 "glamour"
```

Check progress:

```bash
gilgoal status
```

Check whether you can afford a purchase:

```bash
gilgoal afford 80000
```

Export transactions to CSV:

```bash
gilgoal export gil_log.csv --data gil_data.json
```

All data is stored locally in `gil_data.json` (or whatever path you pass with `--path`). Nothing is sent anywhere.

## Tests

```bash
pip install pytest
pytest
```

## License

MIT. Copyright (c) 2026 Asdale Dynamics, LLC. See LICENSE.

## Credit

Created by Asdale Dynamics, LLC (Indiana, formed Oct 2026) — beginner-friendly AI education, books and guides, and practical tools. Find Dylan Asdale's book *The Massive AI Manual* and hub site at dylanasdale.github.io.
