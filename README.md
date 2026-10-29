# ffxiv-gil-goal-cli

A friendly little command-line tool for FFXIV players who want to save up gil for a big purchase — a house, a mount, glamour, or anything else. Set a savings goal, log your earnings and spending, and watch your progress. Everything stays on your computer in a simple JSON file, and you can export your transactions to CSV whenever you like.

Built by **Asdale Dynamics, LLC** — a fan project for FFXIV players. No game assets are included, and this tool is not affiliated with or endorsed by Square Enix.

## Who this is for

Anyone playing Final Fantasy XIV who wants a simple, private way to track gil savings. You don't need to be a programmer. If you can type a command, you can use this tool.

## Install

You'll need Python 3.9 or newer.

```bash
# Download the project
git clone https://github.com/dylanasdale/ffxiv-gil-goal-cli.git
cd ffxiv-gil-goal-cli

# Install the gilgoal command
pip install .
```

That's it. You now have a `gilgoal` command available in your terminal.

Prefer not to install? You can run it straight from the folder:

```bash
python3 -m gilgoal ...
```

## Step by step

**1. Create your data file.** This is where your goal and transactions live (nothing is sent anywhere — it's all local).

```bash
gilgoal init
```

**2. Set your savings goal.** How much gil are you saving for?

```bash
gilgoal set-goal 1000000
```

**3. Log earnings when you make gil.**

```bash
gilgoal earn 150000 "weekly roulettes"
gilgoal earn 80000 "crafting sales"
```

**4. Log spending when you spend gil.**

```bash
gilgoal spend 42000 "glamour"
gilgoal spend 15000 "teleports"
```

**5. Check your progress.**

```bash
gilgoal status
```

You'll see something like:

```
Goal:       1,000,000.00 gil
Earned:     230,000.00 gil
Spent:      57,000.00 gil
Balance:    173,000.00 gil
Remaining:  827,000.00 gil
Progress:   17.3%
```

**6. Check whether you can afford something.**

```bash
gilgoal afford 80000
```

**7. Export your transactions to CSV** (great for a spreadsheet or your own records).

```bash
gilgoal export gil_log.csv --data gil_data.json
```

All data is stored locally in `gildata.json` (or whatever path you pass with `--data`). Nothing is sent anywhere, and no account or personal information is collected.

## Commands at a glance

| Command | What it does |
|---------|--------------|
| `init` | Create a new empty data file |
| `set-goal <amount>` | Set your gil savings goal |
| `earn <amount> [note]` | Log gil you earned |
| `spend <amount> [note]` | Log gil you spent |
| `status` | Show progress toward your goal |
| `afford <amount>` | Check if your balance covers a cost |
| `export <csv-file>` | Export transactions to CSV |

Every command accepts `--data <path>` to use a different JSON data file (default: `gil_data.json`).

## Tests

```bash
pip install pytest
pytest
```

## License

MIT. Copyright (c) 2026 Asdale Dynamics, LLC. See LICENSE.

## Credit

Created by **Asdale Dynamics, LLC** (Indiana, formed Oct 2026) — beginner-friendly AI education, books and guides, and practical tools. Dylan Asdale is a registered nurse turned AI author and founder of Asdale Dynamics, LLC. His book *The Massive AI Manual* and hub site dylanasdale.github.io explain AI "like a friend would": plain English, step by step, never condescending.
