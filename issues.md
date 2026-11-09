# Static Analysis Issues

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| B605: `os.system` with string concatenation | Security (High) | 61 | `os.system("xdg-open " + path)` runs through a shell, so a crafted path can inject commands | Use `subprocess.run([opener, path])` with no shell, and resolve the executable with `shutil.which` |
| B306: `tempfile.mktemp` | Security (Medium) | 55 | `mktemp` returns a name without creating the file, so another process can create it first (race condition) | Use `tempfile.mkstemp`, which creates the file atomically, and close the descriptor |
| B108: hardcoded `/tmp` directory | Security (Medium) | 8 | A fixed `/tmp/expense_reports` path is predictable and insecure on shared systems | Build the path with `tempfile.gettempdir()` and create the folder with `os.makedirs` |
| B105: hardcoded password | Security (Low) | 5 | `BANK_SYNC_PASSWORD = "demo-sync-pass"` keeps a secret in source control | Read it from the `BANK_SYNC_PASSWORD` environment variable and treat an unset value as no match |
| Broad `except Exception` (W0718) | Bug / code quality | 41 | `try/except Exception` in `biggestExpense` can hide unrelated errors | Replaced with `max(..., default=None)`, so no exception handling is needed |
| `global` statement (W0603) | Design | 29 | `setBudget` modifies a module-level variable through `global` | Store the budget in a dict, `budget["monthly"]`, and update it directly |
| camelCase names (C0103) | Style | 11, 20, 28, 33, 38, 44, 49, 53, 59 | Functions, arguments and variables did not follow PEP 8 snake_case | Renamed everything to snake_case and updated every call in `main()` |
| Missing docstrings (C0114, C0116) | Style | 1 and every function | Module and functions had no documentation | Added a docstring to the module and to every function |
| `range(len(...))` loop (C0200) | Style | 45 | Indexing with `range(len(expenses))` is not idiomatic | Used `enumerate(expenses, start=1)` |
| E203, E302, E261, E501 | Style (Flake8) | 15, 44, 74, 77 | Space before `:`, a single blank line between functions, one space before an inline comment, and a line over 79 characters | Removed the space, added the blank line and the extra space, and wrapped long lines |

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 5.27/10 | 10.00/10 |
| Bandit | 4 issues (1 High, 2 Medium, 1 Low) | No issues identified |
| Flake8 | 4 warnings (more after docstrings were added) | 0 warnings |

Note: `# nosec B404` and `# nosec B603` are used on the `subprocess` import and call. The call uses a resolved executable path, a list of arguments and no shell, so the remaining Low findings are accepted risks.
