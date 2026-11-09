# Lab 5: Static Code Analysis - Personal Expense Tracker

**Name:** [your name]  
**SRN:** [your SRN]  
**Section:** [your section]  
**Original repo:** https://github.com/SETAPESU26/L5_32_expense_tracker

## About the program

`expense_tracker.py` is a monthly expense tracker. It records expenses by
category, rejects invalid amounts, totals spending per category, tracks the
remaining budget, finds the biggest expense and checks a bank-sync password.

## How to run

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install pylint bandit flake8
python expense_tracker.py
```

The bank-sync password is no longer hardcoded. It is read from the
`BANK_SYNC_PASSWORD` environment variable. If the variable is not set, every
password check returns `False`.

```bash
export BANK_SYNC_PASSWORD="your-password"
```

## Running the analysis

```bash
python -m pylint expense_tracker.py > pylint_report.txt
python -m bandit -r expense_tracker.py > bandit_report.txt
python -m flake8 expense_tracker.py > flake8_report.txt
```

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 5.27/10 | 10.00/10 |
| Bandit | 4 issues (1 High, 2 Medium, 1 Low) | No issues identified |
| Flake8 | [number from before/flake8_report.txt] warnings | 0 warnings |

The program output is identical before and after the changes.

## Commits

| Commit | Tool | What it fixed |
|--------|------|---------------|
| `87d9dd9` | Bandit | `os.system` shell injection, `mktemp`, hardcoded `/tmp` path, hardcoded password |
| `183135d` | Pylint | snake_case names, docstrings, `global` statement, broad `except`, `range(len())` loop |
| `f5a6be8` | Flake8 | whitespace, blank lines, inline comment spacing, line length |

## Files

- `expense_tracker.py` - the cleaned program
- `issues.md` - the table of issues found and how each was fixed
- `reflection.md` - reflection answers
- `before/` - Pylint, Bandit and Flake8 reports on the original code
- `after/` - the same reports after the fixes

## What I learned

[2 to 4 sentences in your own words: which tool caught what, and one thing
that surprised you.]
