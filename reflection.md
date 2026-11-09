# Reflection

## 1. What did the static analysis tools catch that you might have missed by reading the code?

The program ran correctly, so I would not have noticed several problems by
running it. Bandit flagged `os.system("xdg-open " + path)` as a High-severity
shell injection risk. Because `path` is joined into a string and run through a
shell, a crafted path could execute extra commands. It also flagged
`tempfile.mktemp`, which has a race condition, and a hardcoded password.
Pylint caught the broad `except Exception` and the `global` statement, which
are easy to overlook in working code.

## 2. Did the three tools overlap, or find different kinds of problems?

They found different kinds of problems. Bandit looked for security issues,
Pylint for code quality and design, and Flake8 for PEP 8 formatting. Fixing
one tool's findings did not remove another's. For example, adding docstrings
for Pylint made some lines longer than 79 characters, which Flake8 then
reported. That is why I fixed Bandit first, Pylint second and Flake8 last.

## 3. Did you disagree with any finding, or choose to suppress one?

After replacing `os.system` with `subprocess.run`, Bandit still reported two
Low-severity findings, about importing `subprocess` and calling it. I added
`# nosec B404` and `# nosec B603` to those lines, because the call uses a
resolved executable path, a list of arguments and no shell, so the remaining
risk is small. I understand that `# nosec` hides a warning and does not remove
it, so each suppression needs a reason and I explained mine in `issues.md`.

## 4. How would you use static analysis in a real project?

I would run these tools automatically so problems are caught before code is
merged, for example as a pre-commit hook and in a CI pipeline that fails a
build on new High or Medium Bandit findings or a drop in the Pylint score. I
would also keep one commit per tool, as in this lab, so each round of fixes is
easy to review. One more thing I learned was to check line endings before
committing: converting the file from LF to CRLF made Git show every line as
changed and hid the real fix.
