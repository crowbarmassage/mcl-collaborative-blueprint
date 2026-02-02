# CODING_AGENT_PROMPT.md — MCL Collaborative Blueprint

## Context

You are implementing **MCL Collaborative Blueprint**, a real-time interactive Streamlit dashboard for a 45-person conference. The app has two modes:

1. **Attendee Input (Mobile)** — A wizard-style form where attendees answer 3 strategic questions on their phones
2. **Projector Dashboard (Live)** — An auto-refreshing dashboard visualizing aggregate data with Plotly charts and an AI-powered synthesis engine

Data persists in Google Sheets. The AI synthesis uses OpenAI GPT-4o. Deployment target is Streamlit Community Cloud.

## Current State

The **design phase is complete**. The following files exist in the repo:

- `TECH_SPECS.md` — Full architecture, stack, file structure, and complete starter code for every file
- `ATOMIC_STEPS.md` — 9 implementation phases with atomic steps, evaluation tests, and completion criteria
- `pyproject.toml` — Project configuration
- `requirements.txt` — Pinned dependencies
- `.gitignore` — Standard Python + Streamlit gitignore
- `.pre-commit-config.yaml` — Ruff, mypy, pre-commit hooks
- `.streamlit/config.toml` — Theme and server configuration
- `.streamlit/secrets.toml.example` — Template for credentials
- `.env.example` — Template for local environment variables
- `CHECKPOINT.md` — Progress tracking

## Objective

Implement the application following `ATOMIC_STEPS.md` phase by phase. Each phase must pass its evaluation tests and receive human approval before proceeding.

## Code Standards

Before writing any code, read and follow:
`/Users/mohsin.ansari/Github/PYTHON_STANDARDS.md`

Key requirements:
- Use `uv` for package management
- Run `ruff check` and `ruff format` before commits
- Run `mypy` for type checking
- All functions must have type hints and Google-style docstrings
- Pytest for all tests with >80% coverage target
- Pre-commit hooks must pass

## Constraints

### Architecture
- **Single Streamlit app** — `app.py` is the entry point
- **View routing** via URL query parameter `?mode=admin_dashboard`
- **No sidebar toggle** — dashboard access is URL-only
- **Flat package** at root level — `mcl_blueprint/` (not `src/mcl_blueprint/`) for Streamlit Cloud compatibility

### Data Layer
- **Google Sheets only** — no CSV fallback in production
- Use `st-gsheets-connection` library for all Sheets operations
- Column schema defined in `mcl_blueprint/sheets.py` → `SHEET_COLUMNS`
- All secrets via `st.secrets` (not `os.environ`)

### UI
- **Attendee form**: centered layout, wizard steps via `st.session_state`, thumb-friendly on 375px
- **Dashboard**: wide layout, `streamlit_autorefresh` at 7-second interval
- **AI output**: typewriter effect via `st.empty()` + character-by-character loop

### Testing
- Mock all external dependencies (Google Sheets, OpenAI)
- Streamlit UI components are tested manually (not via pytest)
- Business logic (models, config, visualizations, prompt construction) must have unit tests

## Step Reference

Follow `ATOMIC_STEPS.md` for the complete implementation plan:

| Phase | Focus |
|-------|-------|
| 1 | Foundation — config, models, test fixtures |
| 2 | Google Sheets — read/write data layer |
| 3 | Attendee Form — 3-step mobile wizard |
| 4 | Dashboard — Plotly visualizations |
| 5 | AI Mirror — OpenAI synthesis + typewriter |
| 6 | Integration — end-to-end flow + polish |
| 7 | Deployment — Streamlit Cloud |
| 8 | Notebook — Google Colab demo |
| 9 | Documentation — README, coverage, quality |

## Checkpoint Instructions

After completing each phase:

1. Run the phase's evaluation tests
2. Run `ruff check . && ruff format .`
3. Update `CHECKPOINT.md` with current state
4. Commit with message: `feat: complete phase N — <phase name>`
5. Push to remote
6. Ask for human review before proceeding to next phase

When the session ends (or human says "checkpoint"):

1. Update `CHECKPOINT.md` with exact current state
2. Commit with message: `wip: checkpoint — <current state>`
3. Push to remote

## Resume Protocol

If resuming from a previous session:

1. Read `CHECKPOINT.md`
2. Read `ATOMIC_STEPS.md` to understand where you left off
3. Summarize current state to the human
4. Ask for confirmation before continuing
