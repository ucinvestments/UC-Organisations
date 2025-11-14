# Repository Guidelines

## Project Structure & Module Organization
`app.py` hosts the Flask orchestrator that auto-discovers scraper modules. Shared contracts live in `common/` (`base_scraper.py`, `utils.py`), and each organization keeps its scraper under `handlers/` following UC naming (for example, `handlers/ucop/academic_affairs/scraper.py`). Data persistence is consolidated in `database/` with dedicated folders for schema, models, repositories, and migrations (`migrations/runner.py`). Web assets reside in `templates/` and `static/`, while logs and generated JSON stay inside `logs/` or the organization directories—treat them as generated output when committing.

## Build, Test, and Development Commands
- `python -m venv .venv && source .venv/bin/activate` — set up an isolated environment.
- `pip install -r requirements.txt` — install Flask, BeautifulSoup, and other runtime packages.
- `python app.py` or `flask run` — serve the dashboard at `http://localhost:5000`.
- `docker-compose up --build` — launch the app with its service dependencies.
- `python database/setup.py --init` — create baseline tables; reserve `--reset` for local empty databases.

## Coding Style & Naming Conventions
Follow PEP 8, 4-space indentation, and snake_case for functions and files. Scraper classes should subclass `common.base_scraper.BaseScraper` and use the `{{Org}}Scraper` pattern to stay discoverable. Centralize configuration in `config.py`, pull secrets from `.env` via `python-dotenv`, and avoid embedding credentials. Reuse the logging utilities so timestamps and scraper names appear consistently across files.

## Testing Guidelines
Automated tests are not in place yet; new work should include unit or integration tests under a `tests/` package using `pytest` or `unittest`. Mirror handler paths when naming modules (e.g., `tests/handlers/test_ucop_academic_affairs.py`) and isolate fixtures under `tests/fixtures/`. Exercise database logic against a disposable Neon branch or the Docker Postgres service. Run `python -m pytest` (or the relevant test entry point) before requesting review and note results in the PR description.

## Commit & Pull Request Guidelines
Recent commits are ad-hoc; going forward, use imperative, conventional messages (`feat: add UCOP analytics scraper`) and squash noise before review. Pull requests should outline scope, link issues, summarize manual testing (`python app.py`, `docker-compose up`, etc.), and attach UI screenshots when applicable. Flag new environment variables, migrations, or data outputs prominently so reviewers can stage them.

## Environment & Deployment Notes
Copy `.env.example` to `.env` and supply Flask secrets, Neon URLs, and any API tokens. Respect the rate limits baked into `BaseScraper` and review generated `organization.json` files before committing them. Deployments are container-first: build via the `Dockerfile`, keep `docker-entrypoint.sh` executable, and rotate secrets promptly if logs expose sensitive endpoints.
