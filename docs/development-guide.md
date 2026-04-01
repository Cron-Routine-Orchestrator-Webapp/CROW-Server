# VSHC Development Guide

This guide explains how to set up a local development environment for this project using **uv only**, work inside your fork, and submit changes properly.

The workflow is operating system independent and assumes contribution via a fork.

---

## 1. Fork and Clone the Repository

1. Fork the original repository on GitHub.
2. Clone your fork locally:

```bash
git clone https://github.com/<your-username>/<project_name>.git
cd <project_name>
```

3. Add the upstream repository:

```bash
git remote add upstream https://github.com/<original-owner>/<project_name>.git
```

Verify remotes:

```bash
git remote -v
```

---

## 2. Install uv

Install uv (cross-platform Python package and environment manager).

### macOS / Linux

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```

### Windows (PowerShell)

```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

Verify installation:

```bash
uv --version
```

---

## 3. Create and Use a Virtual Environment

Create a project-local virtual environment:

```bash
uv venv
```

Run commands inside the environment using:

```bash
uv run <command>
```

You do not need to manually activate the environment. Always prefer `uv run` for consistency.

---

## 4. Install Development Dependencies

Install the project and development dependencies:

```bash
uv sync --all-extras
```

---

## 5. Lock Dependencies (Recommended)

Create or update the lockfile:

```bash
uv lock
```

Install exactly what is defined in the lockfile:

```bash
uv sync
```

Commit `uv.lock` to ensure reproducible environments.

---

## 6. Code Quality Checks

Run linting and type checking tools via uv:

```bash
uv run ruff check .
uv run mypy src
```

Fix all reported issues before committing.

---

## 7. Set Up Pre-Commit Hooks

This project uses pre-commit as defined in `.pre-commit-config.yaml`.

Install the Git hooks:

```bash
uv run pre-commit autoupdate
uv run pre-commit install
```

This will automatically run configured checks (e.g. formatting, linting, etc.) on every commit.

To manually run all hooks against the entire repository:

```bash
uv run pre-commit run --all-files
```

If hooks modify files, stage the changes and commit again.

Pre-commit must pass before pushing changes.

---

## 8. Create a Feature Branch

Never work directly on `main`.

```bash
git checkout -b feature/<short-description>
```

Use clear and descriptive branch names.

---

## 9. Make Changes

- Follow the existing `src/` layout.
- Ensure docstrings follow the documented standard.
- Keep commits focused and minimal.
- Always add new dependencies with `uv add <dependency>`

---

## 10. Commit Your Changes

Stage changes:

```bash
git add .
```

Commit with a meaningful message:

```bash
git commit -m "Add: short description of the change"
```

Keep commits atomic and descriptive.

---

## 11. Sync With Upstream

Before pushing, rebase onto the latest upstream main branch:

```bash
git fetch upstream
git rebase upstream/main
```

Resolve conflicts if necessary.

---

## 12. Push to Your Fork

```bash
git push origin feature/<short-description>
```

---

## 13. Open a Pull Request

1. Navigate to your fork on GitHub.
2. Open a Pull Request targeting the original repository's `main` branch.
3. Provide a clear description of:
   - What was changed
   - Why it was changed
   - Any relevant context

Ensure all CI checks pass before requesting review.

---

## 14. Build the Package (Optional)

To build distribution artifacts locally:

```bash
uv build
```

Artifacts will be created in the `dist/` directory.

---

## 15. Files That Must Not Be Committed

Ensure the following are ignored:

- `dist/`
- `*.egg-info/`
- `__pycache__/`
- `.venv/`

Verify they are listed in `.gitignore`.

---

Following this workflow ensures:

- Reproducible environments
- Consistent dependency management
- Clean contribution history
- Cross-platform compatibility
