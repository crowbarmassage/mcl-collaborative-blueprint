# ATOMIC_STEPS.md — MCL Collaborative Blueprint

> Implementation plan organized into phases with atomic steps, starter code, evaluation tests, and completion criteria.

---

## Phase 1: Project Foundation

**Goal**: Set up the project skeleton, configuration constants, data models, and test infrastructure.

### Atomic Steps

- [ ] **1.1** Create directory structure: `mcl_blueprint/`, `mcl_blueprint/components/`, `tests/`
- [ ] **1.2** Create `mcl_blueprint/__init__.py` with version export
- [ ] **1.3** Create `mcl_blueprint/config.py` with all constants (categories, archetypes, thresholds)
- [ ] **1.4** Create `mcl_blueprint/models.py` with `AttendeeResponse` and `AggregatedData` dataclasses
- [ ] **1.5** Create `mcl_blueprint/components/__init__.py`
- [ ] **1.6** Create `tests/__init__.py` and `tests/conftest.py` with shared fixtures
- [ ] **1.7** Create `tests/test_config.py` — verify constants are valid
- [ ] **1.8** Create `tests/test_models.py` — verify dataclass creation and `to_row()`
- [ ] **1.9** Run `ruff check .` and `ruff format .` — fix any issues
- [ ] **1.10** Checkpoint commit: `feat: complete phase 1 — project foundation`

### Files to Create

| File | Purpose |
|------|---------|
| `mcl_blueprint/__init__.py` | Package init with `__version__` |
| `mcl_blueprint/config.py` | All constants and categories |
| `mcl_blueprint/models.py` | `AttendeeResponse`, `AggregatedData` dataclasses |
| `mcl_blueprint/components/__init__.py` | Components subpackage |
| `tests/__init__.py` | Test package |
| `tests/conftest.py` | Shared fixtures |
| `tests/test_config.py` | Config validation tests |
| `tests/test_models.py` | Model tests |

### Starter Code

See `TECH_SPECS.md` — Starter Code section for complete implementations of:
- `mcl_blueprint/__init__.py`
- `mcl_blueprint/config.py`
- `mcl_blueprint/models.py`
- `tests/conftest.py`
- `tests/test_config.py`
- `tests/test_models.py`

### Evaluation Tests

```bash
pytest tests/test_config.py tests/test_models.py -v
```

### Phase 1 Completion Criteria

- [ ] All atomic steps checked off
- [ ] All tests pass: `pytest tests/test_config.py tests/test_models.py -v`
- [ ] Code passes linting: `ruff check mcl_blueprint/ tests/`
- [ ] Human review approved

---

## Phase 2: Google Sheets Integration

**Goal**: Implement the data layer — reading all responses and writing new submissions to Google Sheets.

### Atomic Steps

- [ ] **2.1** Create `mcl_blueprint/sheets.py` with `SHEET_COLUMNS`, `get_connection()`, `read_all_responses()`, `write_response()`
- [ ] **2.2** Create the Google Sheet manually with correct column headers (document in README)
- [ ] **2.3** Configure `.streamlit/secrets.toml` locally with service account credentials
- [ ] **2.4** Create `tests/test_sheets.py` — mock-based tests for read/write
- [ ] **2.5** Verify connection works with a manual test (read empty sheet, write one row, read back)
- [ ] **2.6** Checkpoint commit: `feat: complete phase 2 — google sheets integration`

### Files to Create

| File | Purpose |
|------|---------|
| `mcl_blueprint/sheets.py` | Google Sheets read/write operations |
| `tests/test_sheets.py` | Mocked sheets tests |

### Starter Code

See `TECH_SPECS.md` — `mcl_blueprint/sheets.py` for complete implementation.

**tests/test_sheets.py**:
```python
"""Tests for Google Sheets data layer (mocked)."""

from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from mcl_blueprint.sheets import SHEET_COLUMNS, read_all_responses, write_response


class TestSheetColumns:
    """Verify sheet column definitions."""

    def test_columns_start_with_session_id(self) -> None:
        assert SHEET_COLUMNS[0] == "session_id"

    def test_columns_include_all_budget_fields(self) -> None:
        budget_cols = [c for c in SHEET_COLUMNS if c.startswith("q1_") and c != "q1_reasoning"]
        assert len(budget_cols) == 7  # 7 priority categories


class TestReadAllResponses:
    """Tests for reading from Google Sheets."""

    @patch("mcl_blueprint.sheets.get_connection")
    def test_returns_dataframe(self, mock_conn: MagicMock) -> None:
        mock_conn.return_value.read.return_value = pd.DataFrame(columns=SHEET_COLUMNS)
        df = read_all_responses()
        assert isinstance(df, pd.DataFrame)

    @patch("mcl_blueprint.sheets.get_connection")
    def test_empty_sheet_returns_empty_df(self, mock_conn: MagicMock) -> None:
        mock_conn.return_value.read.return_value = pd.DataFrame()
        df = read_all_responses()
        assert df.empty


class TestWriteResponse:
    """Tests for writing to Google Sheets."""

    @patch("mcl_blueprint.sheets.read_all_responses")
    @patch("mcl_blueprint.sheets.get_connection")
    def test_write_calls_update(self, mock_conn: MagicMock, mock_read: MagicMock) -> None:
        mock_read.return_value = pd.DataFrame(columns=SHEET_COLUMNS)
        row = ["test-id", "2026-02-01T00:00:00"] + ["0"] * (len(SHEET_COLUMNS) - 2)
        write_response(row)
        mock_conn.return_value.update.assert_called_once()
```

### Evaluation Tests

```bash
pytest tests/test_sheets.py -v
```

### Phase 2 Completion Criteria

- [ ] All atomic steps checked off
- [ ] All tests pass: `pytest tests/test_sheets.py -v`
- [ ] Manual verification: write and read back one row from Google Sheets
- [ ] Code passes linting: `ruff check mcl_blueprint/sheets.py`
- [ ] Human review approved

---

## Phase 3: Attendee Mobile Form

**Goal**: Build the 3-step wizard form for mobile attendees, writing responses to Google Sheets on completion.

### Atomic Steps

- [ ] **3.1** Create `mcl_blueprint/components/attendee.py` with `render_attendee_form()` and step renderers
- [ ] **3.2** Implement Step 1: Priority Budget — 7 sliders summing to 100, credits counter, reasoning text area
- [ ] **3.3** Implement Step 2: Threat Matrix — dropdown (+ Other), likelihood slider, impact slider, trigger input
- [ ] **3.4** Implement Step 3: AI Alignment — archetype selection buttons, conditional follow-up input
- [ ] **3.5** Implement thank-you screen with `st.balloons()`
- [ ] **3.6** Wire up `write_response()` call on final submission
- [ ] **3.7** Test full wizard flow locally: `streamlit run app.py`
- [ ] **3.8** Verify response appears in Google Sheet
- [ ] **3.9** Test on mobile viewport (Chrome DevTools → responsive mode, 375px width)
- [ ] **3.10** Checkpoint commit: `feat: complete phase 3 — attendee mobile form`

### Files to Create

| File | Purpose |
|------|---------|
| `mcl_blueprint/components/attendee.py` | 3-step wizard form |
| `app.py` | Main entry point (routes to attendee or dashboard) |

### Starter Code

See `TECH_SPECS.md` for complete implementations of:
- `app.py`
- `mcl_blueprint/components/attendee.py`

### Evaluation Tests

Manual testing (Streamlit UI cannot be unit tested easily):

```bash
# Run the app locally
streamlit run app.py

# 1. Open http://localhost:8501
# 2. Complete all 3 steps
# 3. Verify data appears in Google Sheet
# 4. Test mobile viewport in Chrome DevTools
```

### Phase 3 Completion Criteria

- [ ] All atomic steps checked off
- [ ] Wizard completes all 3 steps without errors
- [ ] Budget sliders enforce total = 100
- [ ] Data successfully written to Google Sheet
- [ ] UI is thumb-friendly on 375px mobile viewport
- [ ] Code passes linting: `ruff check mcl_blueprint/components/attendee.py`
- [ ] Human review approved

---

## Phase 4: Dashboard Visualizations

**Goal**: Build the projector dashboard with live Plotly charts for all 3 questions and auto-refresh.

### Atomic Steps

- [ ] **4.1** Create `mcl_blueprint/visualizations.py` with `build_priority_bar_chart()`, `build_threat_scatter()`, `build_archetype_grid()`
- [ ] **4.2** Create `mcl_blueprint/components/dashboard.py` with `render_dashboard()` and `_aggregate()`
- [ ] **4.3** Wire up `streamlit_autorefresh` at 7-second interval
- [ ] **4.4** Implement Q1 visualization: horizontal bar chart sorted high-to-low
- [ ] **4.5** Implement Q2 visualization: scatter plot with 4 colored quadrants and hover tooltips
- [ ] **4.6** Implement Q3 visualization: 2x2 heatmap grid with dominant archetype highlighted
- [ ] **4.7** Add `st.metric` for total response count
- [ ] **4.8** Create `tests/test_visualizations.py` — verify chart construction
- [ ] **4.9** Test dashboard locally: `streamlit run app.py` → append `?mode=admin_dashboard`
- [ ] **4.10** Submit 3-5 test responses via attendee form, verify charts update
- [ ] **4.11** Checkpoint commit: `feat: complete phase 4 — dashboard visualizations`

### Files to Create

| File | Purpose |
|------|---------|
| `mcl_blueprint/visualizations.py` | Plotly chart builders |
| `mcl_blueprint/components/dashboard.py` | Dashboard layout and aggregation |
| `tests/test_visualizations.py` | Chart construction tests |

### Starter Code

See `TECH_SPECS.md` for complete implementations of:
- `mcl_blueprint/visualizations.py`
- `mcl_blueprint/components/dashboard.py`
- `tests/test_visualizations.py`

### Evaluation Tests

```bash
pytest tests/test_visualizations.py -v
```

Plus manual testing:
```bash
streamlit run app.py
# Navigate to http://localhost:8501/?mode=admin_dashboard
# Verify charts render with test data
```

### Phase 4 Completion Criteria

- [ ] All atomic steps checked off
- [ ] All tests pass: `pytest tests/test_visualizations.py -v`
- [ ] Dashboard renders all 3 chart sections
- [ ] Auto-refresh cycles every 7 seconds
- [ ] Charts update when new responses are submitted
- [ ] Hover tooltips work on scatter plot
- [ ] Code passes linting: `ruff check mcl_blueprint/visualizations.py mcl_blueprint/components/dashboard.py`
- [ ] Human review approved

---

## Phase 5: AI Mirror Synthesis

**Goal**: Integrate OpenAI GPT-4o to generate strategic tactics with a typewriter display effect.

### Atomic Steps

- [ ] **5.1** Create `mcl_blueprint/ai_mirror.py` with `build_synthesis_prompt()`, `generate_synthesis()`, `render_typewriter()`
- [ ] **5.2** Add "Generate Strategic Blueprint" button to dashboard
- [ ] **5.3** Implement prompt construction from aggregated data (top priority, top threat, dominant archetype)
- [ ] **5.4** Implement OpenAI API call with error handling
- [ ] **5.5** Implement typewriter effect using `st.empty()` character-by-character display
- [ ] **5.6** Create `tests/test_ai_mirror.py` — verify prompt construction (mocked API)
- [ ] **5.7** Test end-to-end: submit responses → view dashboard → click "Generate" → see typewriter output
- [ ] **5.8** Checkpoint commit: `feat: complete phase 5 — ai mirror synthesis`

### Files to Create

| File | Purpose |
|------|---------|
| `mcl_blueprint/ai_mirror.py` | OpenAI synthesis + typewriter display |
| `tests/test_ai_mirror.py` | Prompt construction tests |

### Starter Code

See `TECH_SPECS.md` for complete implementations of:
- `mcl_blueprint/ai_mirror.py`
- `tests/test_ai_mirror.py`

### Evaluation Tests

```bash
pytest tests/test_ai_mirror.py -v
```

Plus manual testing:
```bash
# Ensure OPENAI_API_KEY is set in .streamlit/secrets.toml
streamlit run app.py
# Navigate to dashboard, click "Generate Strategic Blueprint"
# Verify typewriter animation displays 3-sentence tactic
```

### Phase 5 Completion Criteria

- [ ] All atomic steps checked off
- [ ] All tests pass: `pytest tests/test_ai_mirror.py -v`
- [ ] Prompt includes all three data points (priority, threat, archetype)
- [ ] Typewriter animation displays character by character
- [ ] Error handling works when API key is missing
- [ ] Code passes linting: `ruff check mcl_blueprint/ai_mirror.py`
- [ ] Human review approved

---

## Phase 6: Integration & Polish

**Goal**: End-to-end verification, error handling, and mobile responsiveness polish.

### Atomic Steps

- [ ] **6.1** Test full flow: attendee form → Google Sheets → dashboard → AI synthesis
- [ ] **6.2** Test with 5+ concurrent submissions (open multiple browser tabs)
- [ ] **6.3** Verify dashboard shows "Waiting for responses..." when sheet is empty
- [ ] **6.4** Verify graceful error when Google Sheets is unreachable
- [ ] **6.5** Verify graceful error when OpenAI API key is invalid
- [ ] **6.6** Test mobile form on actual phone (same WiFi, use local IP)
- [ ] **6.7** Fine-tune chart colors, fonts, and layout for projector readability
- [ ] **6.8** Create `tests/test_integration.py` — mocked end-to-end flow
- [ ] **6.9** Run full test suite: `pytest tests/ -v`
- [ ] **6.10** Run `ruff check . && ruff format .`
- [ ] **6.11** Checkpoint commit: `feat: complete phase 6 — integration and polish`

### Files to Create

| File | Purpose |
|------|---------|
| `tests/test_integration.py` | End-to-end flow tests (mocked) |

### Starter Code

**tests/test_integration.py**:
```python
"""Integration tests for MCL Collaborative Blueprint.

Tests the full data flow from attendee response to dashboard aggregation.
All external dependencies (Google Sheets, OpenAI) are mocked.
"""

from unittest.mock import patch

import pandas as pd
import pytest

from mcl_blueprint.ai_mirror import build_synthesis_prompt
from mcl_blueprint.config import PRIORITY_CATEGORIES
from mcl_blueprint.models import AttendeeResponse
from mcl_blueprint.sheets import SHEET_COLUMNS


class TestEndToEndFlow:
    """Test the complete data pipeline."""

    def test_response_to_row_matches_sheet_columns(self, sample_response: AttendeeResponse) -> None:
        """Verify AttendeeResponse.to_row() produces correct column count."""
        row = sample_response.to_row()
        assert len(row) == len(SHEET_COLUMNS)

    def test_aggregation_produces_synthesis_inputs(self, sample_aggregated_data) -> None:
        """Verify aggregation provides all data needed for AI synthesis."""
        assert sample_aggregated_data.top_priority != ""
        assert sample_aggregated_data.top_threat != ""
        assert sample_aggregated_data.dominant_archetype != ""

    def test_full_pipeline_prompt_is_valid(self, sample_aggregated_data) -> None:
        """Verify the synthesis prompt is well-formed from aggregated data."""
        prompt = build_synthesis_prompt(sample_aggregated_data)
        assert len(prompt) > 50
        assert "Guerilla Tactic" in prompt
```

### Evaluation Tests

```bash
pytest tests/ -v
```

### Phase 6 Completion Criteria

- [ ] All atomic steps checked off
- [ ] Full test suite passes: `pytest tests/ -v`
- [ ] Full flow works: form → sheets → dashboard → AI
- [ ] Mobile form is usable on a real phone
- [ ] Dashboard is readable on a projector
- [ ] Error states handled gracefully
- [ ] Code passes linting: `ruff check .`
- [ ] Human review approved

---

## Phase 7: Streamlit Cloud Deployment

**Goal**: Deploy to Streamlit Community Cloud and verify production functionality.

### Atomic Steps

- [ ] **7.1** Push all code to GitHub
- [ ] **7.2** Log in to share.streamlit.io
- [ ] **7.3** Create new app: select repo, branch `main`, main file `app.py`
- [ ] **7.4** Configure secrets in Streamlit Cloud dashboard (copy from `secrets.toml`)
- [ ] **7.5** Verify attendee URL works: `https://<app-name>.streamlit.app`
- [ ] **7.6** Verify dashboard URL works: `https://<app-name>.streamlit.app/?mode=admin_dashboard`
- [ ] **7.7** Submit a test response on mobile, verify it appears on dashboard
- [ ] **7.8** Test AI synthesis button on deployed dashboard
- [ ] **7.9** Generate QR code for the attendee URL
- [ ] **7.10** Checkpoint commit: `feat: complete phase 7 — streamlit cloud deployment`

### Files to Create

No new files — deployment configuration only.

### Evaluation Tests

Manual verification:
1. Attendee form loads on mobile browser
2. All 3 wizard steps complete without errors
3. Dashboard auto-refreshes and shows new data
4. AI synthesis generates and displays with typewriter effect
5. QR code resolves to correct URL

### Phase 7 Completion Criteria

- [ ] App is live on Streamlit Community Cloud
- [ ] Both URLs work (attendee + dashboard)
- [ ] Full flow verified on deployed app
- [ ] QR code generated and tested
- [ ] Human review approved

---

## Phase 8: Notebook & Demo

**Goal**: Create a Google Colab-compatible notebook demonstrating the project.

### Atomic Steps

- [ ] **8.1** Create `notebooks/` directory
- [ ] **8.2** Create `notebooks/demo.ipynb` with standard structure
- [ ] **8.3** Include setup cell (clone repo, install dependencies)
- [ ] **8.4** Include API key configuration cell (Colab Secrets + fallback)
- [ ] **8.5** Include demo cells showing data model usage, chart generation, and prompt construction
- [ ] **8.6** Add markdown explanations for each step
- [ ] **8.7** Verify notebook runs on Google Colab
- [ ] **8.8** Checkpoint commit: `docs: complete phase 8 — demo notebook`

### Files to Create

| File | Purpose |
|------|---------|
| `notebooks/demo.ipynb` | Google Colab demo notebook |

### Evaluation Tests

Manual verification:
1. Push code to GitHub
2. Open notebook in Google Colab
3. Run all cells
4. Verify outputs are correct

### Phase 8 Completion Criteria

- [ ] Notebook exists at `notebooks/demo.ipynb`
- [ ] Notebook runs successfully on Google Colab
- [ ] All cells execute without errors
- [ ] Markdown explanations are clear
- [ ] Human review approved

---

## Phase 9: Documentation & Quality

**Goal**: Finalize README, verify test coverage, and ensure all quality checks pass.

### Atomic Steps

- [ ] **9.1** Finalize `README.md` with installation, usage, and deployment instructions
- [ ] **9.2** Run full test suite with coverage: `pytest tests/ -v --cov=mcl_blueprint --cov-report=term-missing`
- [ ] **9.3** Verify coverage ≥ 80% (excluding Streamlit UI code which is manually tested)
- [ ] **9.4** Run `ruff check . && ruff format --check .`
- [ ] **9.5** Run `mypy mcl_blueprint/` (note: some Streamlit types may need `# type: ignore`)
- [ ] **9.6** Update `CHECKPOINT.md` to reflect project completion
- [ ] **9.7** Final commit: `docs: complete phase 9 — documentation and quality`

### Files to Create

No new files — updates only.

### Evaluation Tests

```bash
# Full quality check
ruff check .
ruff format --check .
mypy mcl_blueprint/
pytest tests/ -v --cov=mcl_blueprint --cov-report=term-missing
```

### Phase 9 Completion Criteria

- [ ] README is complete with all sections
- [ ] Test coverage ≥ 80%
- [ ] Ruff passes with no errors
- [ ] All tests pass
- [ ] CHECKPOINT.md reflects completion
- [ ] Human review approved

---

## Progress Tracking

| Phase | Status | Tests Pass | Human Approved | Notes |
|-------|--------|------------|----------------|-------|
| 1. Foundation | [ ] | [ ] | [ ] | Config + models + fixtures |
| 2. Google Sheets | [ ] | [ ] | [ ] | Data layer |
| 3. Attendee Form | [ ] | [ ] | [ ] | Mobile wizard (manual test) |
| 4. Dashboard Viz | [ ] | [ ] | [ ] | Plotly charts |
| 5. AI Mirror | [ ] | [ ] | [ ] | OpenAI synthesis |
| 6. Integration | [ ] | [ ] | [ ] | End-to-end + polish |
| 7. Deployment | [ ] | [ ] | [ ] | Streamlit Cloud |
| 8. Notebook | [ ] | [ ] | [ ] | **Required** |
| 9. Documentation | [ ] | [ ] | [ ] | Quality checks |

---

## Quick Reference: Test Commands

| Phase | Command |
|-------|---------|
| Phase 1 | `pytest tests/test_config.py tests/test_models.py -v` |
| Phase 2 | `pytest tests/test_sheets.py -v` |
| Phase 3 | Manual: `streamlit run app.py` |
| Phase 4 | `pytest tests/test_visualizations.py -v` |
| Phase 5 | `pytest tests/test_ai_mirror.py -v` |
| Phase 6 | `pytest tests/ -v` |
| Phase 7 | Manual: verify deployed URLs |
| Phase 8 | Manual: run notebook on Google Colab |
| Phase 9 | `pytest tests/ -v --cov=mcl_blueprint --cov-fail-under=80` |
| All | `pytest tests/ -v --cov=mcl_blueprint` |
