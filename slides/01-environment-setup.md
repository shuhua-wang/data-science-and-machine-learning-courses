---
theme: penguin
title: Module 1 — Environment Setup & Tooling
author: Data Science & Machine Learning Course
info: |
  Module 1 of the Data Science & Machine Learning course.
  Getting from a blank computer to a working, reproducible Python environment with uv.
transition: fade
---

---
layout: intro
---

# Data Science and Machine Learning
Hands-on Tutorial

---
layout: presenter
presenterImage: 'https://res.cloudinary.com/alvarosaburido/image/upload/v1622370075/as-portfolio/alvaro_saburido.jpg'
---

- Shuhua Wang
- Senior Data Engineer
- Ovintiv

---

# Module 1
## Environment Setup & Tooling

Installing `uv` and setting up a reproducible Python environment

---

# Lessons in this module

1. What is a Terminal, and What is Python?
2. Installing `uv` (macOS, Linux, and Windows)
3. Managing Python Versions with `uv`
4. Managing Packages & Projects with `uv`
5. Setting Up an Editor and Jupyter

By the end: a working `uv` project, an editor, and Jupyter — ready for Module 2.

---
layout: center
---

# Lesson 1.1
## What is a Terminal, and What is Python?

---

# GUI vs. terminal

- **GUI** (Graphical User Interface) — click buttons and icons
- **Terminal** — type text commands, read text responses
- The program that runs your commands is called a **shell**

Why use it?

- **Precise** — one line, no misclicks
- **Repeatable** — save & rerun the exact same steps
- **It's how Python, `uv`, and Jupyter actually work**

---

# Opening a terminal

| OS | App |
|---|---|
| macOS | **Terminal** (`Cmd+Space` → "Terminal") |
| Linux | **Terminal** / **Konsole** / `Ctrl+Alt+T` |
| Windows | **PowerShell** |

```text
yourname@yourcomputer ~ %        ← macOS/Linux prompt
PS C:\Users\yourname>            ← Windows prompt
```

---

# Navigation commands

```bash
pwd        # where am I?
ls         # what's here?  (Windows: dir)
cd notebooks   # move into a folder
cd ..          # move up one level
cd ~           # jump to home
```

- **Absolute path**: `/Users/yourname/projects/...`
- **Relative path**: `notebooks` (from where you are now)
- Spaces in a name? Quote it: `cd "My Project"`
- macOS/Windows: case-*insensitive*. Linux: case-*sensitive*.

---

# What is Python?

- A programming language, designed to read like plain English
- Code lives in a **script**: a plain text `.py` file
- Python is **interpreted** — the **interpreter** reads and runs
  your code line by line (no separate compile step)

```bash
python hello.py
```
```text
Hello, world!
```

---

# The REPL

Run `python` with no file → interactive prompt:

```text
>>> 2 + 2
4
>>> print("hi")
hi
>>> exit()
```

A Jupyter notebook (Lesson 1.5) is this same idea, in editable, re-runnable cells.

`python` vs `python3`: inconsistent across OSes — `uv` fixes this for us starting
next lesson.

---
layout: center
---

# Lesson 1.2
## Installing `uv`

---

# What is `uv`, and why use it?

`uv` = one fast tool that installs Python versions, creates isolated project
environments, installs packages, and locks exact versions.

Replaces juggling `pip` + `venv` + `pyenv` (+ `conda`) separately.

- **One tool**, one mental model
- **Fast** — 10–100x faster installs than `pip`
- **Reproducible** — writes a lockfile automatically
- **Never touches your system Python**

---

# Install: macOS / Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```text
downloading uv 0.12.3 aarch64-apple-darwin
installing to /Users/yourname/.local/bin
everything's installed!
```

macOS + Homebrew alternative: `brew install uv`

Close & reopen your terminal afterward.

---

# Install: Windows

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

```text
downloading uv 0.12.3 x86_64-pc-windows-msvc
installing to C:\Users\yourname\.local\bin
everything's installed!
```

Alternative: `winget install --id=astral-sh.uv -e`

Close & reopen PowerShell afterward.

---

# Verify the install

```bash
uv --version
```
```text
uv 0.12.3 (aarch64-apple-darwin)
```

If you see **"command not found: uv"** (or PowerShell's "not recognized"), it's a
**PATH** problem — your shell doesn't know where `uv` lives.

---

# Fixing PATH issues

**What is PATH?** A list of folders your shell searches for commands.

- **macOS/Linux**: reopen terminal, or `source ~/.zshrc` (`~/.bashrc` on many
  Linux setups); confirm `~/.local/bin` is exported onto `PATH`
- **Windows**: reopen PowerShell; else Start Menu → "Environment Variables" →
  edit `Path` → add `...\​.local\bin`

Try it yourself: `notebooks/1.2-installing-uv.ipynb`

---
layout: center
---

# Lesson 1.3
## Managing Python Versions with `uv`

---

# Why pin a Python version?

- Python changes over time (3.10, 3.11, 3.12, ...)
- Your code, or a package, may need a specific version
- **Pinning** records the exact version a project expects — so
  everyone (including future you) gets the same one automatically

Same reproducibility idea as the lockfile in Lesson 1.4, applied to Python itself.

---

# List & install versions

```bash
uv python list
```
```text
cpython-3.13.2-macos-aarch64-none   <download available>
cpython-3.10.12-macos-aarch64-none  /Users/yourname/.local/bin/python3.10
```

```bash
uv python install 3.12
```
```text
Installed Python 3.12.8 in 2.1s
```

`uv` downloads and manages versions itself — no separate python.org install needed.

---

# Pin a version to a project

```bash
uv python pin 3.10
```
```text
Pinned `.python-version` to `cpython-3.10.12-macos-aarch64-none`
```

```bash
cat .python-version
```
```text
3.10
```

This file is committed to version control — every collaborator gets the same
interpreter.

---

# Per-project switching

```bash
cd project-a   # pinned 3.10
uv run python --version    # → Python 3.10.12

cd project-b   # pinned 3.12
uv run python --version    # → Python 3.12.8
```

No activating, no deactivating — `uv` reads each folder's pin automatically.

Try it yourself: `notebooks/1.3-managing-python-versions.ipynb`

---
layout: center
---

# Lesson 1.4
## Managing Packages & Projects with `uv`

---

# Packages & version conflicts

- A **package** = reusable published code (`pandas`, `scikit-learn`, ...)
- Packages depend on other packages, which have their own versions
- **Version conflict**: two things you need disagree on a shared
  dependency's version

Fix: give every project its **own isolated environment** (`.venv`) —
`uv` creates and manages this for you.

---

# `uv init` — start a new project

```bash
mkdir my-first-project && cd my-first-project
uv init
```

```text
my-first-project/
├── .python-version
├── pyproject.toml   ← the project's "ID card"
├── README.md
└── main.py
```

---

# `uv add` — add a dependency

```bash
uv add pandas
```
```text
Resolved 12 packages in 320ms
Installed 6 packages in 89ms
 + numpy==2.2.6
 + pandas==2.3.3
 ...
```

- Resolves compatible versions
- Installs into the project's isolated environment
- Updates `pyproject.toml` **and** `uv.lock`
- Dev-only tools: `uv add --dev jupyter`

---

# `uv run` and `uv sync`

```bash
uv run python main.py       # run inside the project's own environment
```

```bash
uv sync                     # recreate the environment from
                             # pyproject.toml + uv.lock, exactly
```

`uv run` = "do this, using exactly this project's packages & Python."
`uv sync` = "make my environment match what's recorded, exactly."

---

# What is `uv.lock`, and why commit it?

- `pyproject.toml` says *what you want* (roughly — version ranges)
- `uv.lock` says *exactly what you got* — every package, exact version,
  down to the last patch number
- Commit it to version control (`git`) → everyone gets a
  **byte-for-byte identical environment**, forever

Never hand-edit `uv.lock` — change deps with `uv add` / `uv remove`.

---

# This repo already has an environment!

Everything above is the workflow for a **brand-new project of your own.**

For **this course's repo**, `pyproject.toml` + `uv.lock` already exist — just run:

```bash
cd data-science-courses
uv sync
```

That's the *only* command you need here. Then use `uv run ...` for everything.

Try it yourself: `notebooks/1.4-managing-packages-and-projects.ipynb`

---
layout: center
---

# Lesson 1.5
## Setting Up an Editor and Jupyter

---

# VS Code

1. Download from **code.visualstudio.com**, install
2. Extensions panel → install **"Python"** (Microsoft)
3. Optional: `code .` opens the current folder in VS Code
   - Not found? `Cmd/Ctrl+Shift+P` → "Install 'code' command in PATH"

Any editor works — VS Code is just the one with guided setup here.

---

# Adding Jupyter

```bash
uv add --dev jupyter
```
```text
Resolved 38 packages in 210ms
Installed 38 packages in 3.4s
 + jupyter==1.1.1
 + ipykernel==7.3.0
```

`.ipynb` notebook = formatted text + live code + output, in runnable **cells**.

(Already installed in this course's repo — no need to run this here.)

---

# Launching a notebook

```bash
uv run jupyter lab
```
```text
Jupyter Server is running at:
http://localhost:8888/lab?token=8f2e1c9a...
```

Or: install the **"Jupyter"** extension in VS Code and open any `.ipynb` directly.

Pick the kernel pointing at this project's `.venv` — that's what guarantees the
right packages.

---

# You're ready

- `Shift+Enter` runs a cell and moves to the next
- "Run All Cells" runs a whole notebook top to bottom
- `ModuleNotFoundError` on something installed? → wrong kernel selected

Try it yourself: `notebooks/1.5-editor-and-jupyter-setup.ipynb`

---
layout: center
---

# Module 1 complete

Terminal ✓ · `uv` ✓ · Python versions ✓ · Project & packages ✓ · Editor & Jupyter ✓

On to **Module 2: Python Programming Basics**
