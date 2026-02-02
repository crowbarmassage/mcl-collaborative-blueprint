# TECH_SPECS.md — MCL Collaborative Blueprint

## Overview

MCL Collaborative Blueprint is a real-time interactive Streamlit dashboard for a 45-person conference. It serves two simultaneous user groups via a single codebase:

Key capabilities:
1. **Attendee Input (Mobile)** — A thumb-friendly wizard-style form where attendees answer 3 strategic questions via their phones
2. **Projector Dashboard (Live)** — An auto-refreshing full-screen dashboard that visualizes aggregate data with Plotly charts
3. **AI Mirror (Synthesis)** — An OpenAI-powered engine that generates a strategic "Guerilla Tactic" from the room's collective data

The system uses a Streamlit single-page app where the view mode is toggled via a URL query parameter (`?mode=admin_dashboard`). Google Sheets serves as the shared data layer, ensuring persistence and real-time concurrency for 45 users on Streamlit Community Cloud.

---

## Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Language | Python 3.11+ | Core implementation |
| UI Framework | Streamlit >=1.40 | Web interface for both mobile and projector views |
| Charts | Plotly Express >=5.24 | Interactive bar, scatter, and heatmap visualizations |
| Data Layer | Google Sheets via `st-gsheets-connection` | Persistent, concurrent storage for 45 users |
| AI | OpenAI API (GPT-4o) via `openai` >=1.50 | Strategic synthesis engine |
| Auto-Refresh | `streamlit-autorefresh` >=1.0 | Dashboard auto-polls every 5-10 seconds |
| Data Processing | Pandas >=2.2 | Aggregation and transformation of responses |
| Package Manager | uv | Dependency management |
| Linting | ruff | Code quality |
| Type Checking | mypy | Static analysis |
| Testing | pytest | Test framework |
| Deployment | Streamlit Community Cloud | Free SSL-secured hosting |

---

## File Structure

```
mcl-collaborative-blueprint/
├── app.py                              # Streamlit entry point — routes to attendee or dashboard
├── mcl_blueprint/                      # Application package
│   ├── __init__.py                     # Package exports
│   ├── config.py                       # Constants, categories, archetypes, settings
│   ├── models.py                       # Dataclasses for responses and aggregations
│   ├── sheets.py                       # Google Sheets read/write via st-gsheets-connection
│   ├── visualizations.py              # Plotly chart builders (bar, scatter, heatmap)
│   ├── ai_mirror.py                    # OpenAI synthesis engine with typewriter effect
│   └── components/
│       ├── __init__.py
│       ├── attendee.py                 # Mobile form: wizard steps for Q1, Q2, Q3
│       └── dashboard.py               # Projector view: charts + AI synthesis panel
├── tests/
│   ├── __init__.py
│   ├── conftest.py                     # Shared fixtures (mock sheets, mock openai)
│   ├── test_config.py                  # Test constants and categories
│   ├── test_models.py                  # Test data models and validation
│   ├── test_sheets.py                  # Test Google Sheets read/write (mocked)
│   ├── test_visualizations.py         # Test chart generation
│   ├── test_ai_mirror.py              # Test prompt construction and output
│   └── test_integration.py            # End-to-end flow tests
├── .streamlit/
│   ├── config.toml                     # Streamlit theme and server config
│   └── secrets.toml.example            # Template for secrets (actual file gitignored)
├── notebooks/
│   └── demo.ipynb                      # Google Colab demo notebook
├── .env                                # Local env vars (gitignored)
├── .env.example                        # Template for .env
├── .gitignore
├── .pre-commit-config.yaml
├── pyproject.toml
├── requirements.txt
├── repo_details.json
├── TECH_SPECS.md
├── ATOMIC_STEPS.md
├── FUTURE_FEATURES.md
├── CODING_AGENT_PROMPT.md
├── CHECKPOINT.md
└── README.md
```

---

## Environment Variables

All secrets are managed via Streamlit's `st.secrets` for production (Streamlit Community Cloud) and `.env` for local development.

| Variable | Location | Description | Required |
|----------|----------|-------------|----------|
| `OPENAI_API_KEY` | `secrets.toml` | OpenAI API key for GPT-4o synthesis | Yes |
| `connections.gsheets.spreadsheet` | `secrets.toml` | Google Sheet URL | Yes |
| `connections.gsheets.type` | `secrets.toml` | Must be `"service_account"` | Yes |
| `connections.gsheets.project_id` | `secrets.toml` | GCP project ID | Yes |
| `connections.gsheets.private_key` | `secrets.toml` | Service account private key | Yes |
| `connections.gsheets.client_email` | `secrets.toml` | Service account email | Yes |

**Note**: On Streamlit Community Cloud, secrets are configured in the app dashboard under "Secrets". Locally, create `.streamlit/secrets.toml` from the example file.

---

## Starter Code

### `app.py`

```python
"""MCL Collaborative Blueprint — Main Streamlit entry point.

Routes between Attendee Input (mobile) and Admin Dashboard (projector)
based on the URL query parameter `?mode=admin_dashboard`.
"""

import streamlit as st

from mcl_blueprint.components.attendee import render_attendee_form
from mcl_blueprint.components.dashboard import render_dashboard
from mcl_blueprint.config import APP_TITLE, DASHBOARD_MODE_KEY


def main() -> None:
    """Main entry point. Route based on query parameter."""
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon="🏛️",
        layout="wide" if _is_dashboard_mode() else "centered",
    )

    if _is_dashboard_mode():
        render_dashboard()
    else:
        render_attendee_form()


def _is_dashboard_mode() -> bool:
    """Check if the URL contains ?mode=admin_dashboard."""
    params = st.query_params
    return params.get("mode", "") == DASHBOARD_MODE_KEY


if __name__ == "__main__":
    main()
```

### `mcl_blueprint/__init__.py`

```python
"""MCL Collaborative Blueprint — Real-time conference dashboard."""

__version__ = "0.1.0"
```

### `mcl_blueprint/config.py`

```python
"""Configuration constants for MCL Collaborative Blueprint."""

# App
APP_TITLE = "MCL 2026 — Collaborative Blueprint"
DASHBOARD_MODE_KEY = "admin_dashboard"
DASHBOARD_REFRESH_INTERVAL_MS = 7000  # 7 seconds

# Q1: Priority Budget
TOTAL_CREDITS = 100
PRIORITY_CATEGORIES: list[str] = [
    "Chaplaincy",
    "Prayer Space",
    "Halal Food",
    "Mental Health",
    "Admin Access",
    "Security/Safety",
    "Legal Defense",
]

# Q2: Threat Matrix
THREAT_OPTIONS: list[str] = [
    "Budget Cuts",
    "Doxxing",
    "Protest Bans",
    "Surveillance",
    "Apathy",
]
LIKELIHOOD_RANGE: tuple[int, int] = (1, 10)
IMPACT_RANGE: tuple[int, int] = (1, 10)

# Q3: AI Alignment Archetypes
ARCHETYPES: dict[str, str] = {
    "The Fortress": "Bans, Detection Software",
    "The Ostrich": "No Policy, Confusion",
    "The Lab": "Experimentation, Training",
    "The Watchtower": "Surveillance, Monitoring",
}

# Conditional follow-up questions per archetype
ARCHETYPE_FOLLOWUPS: dict[str, str] = {
    "The Fortress": "How does the ban hurt advocacy?",
    "The Ostrich": "What risk does this vacuum create?",
    "The Lab": "What experiment would you run first?",
    "The Watchtower": "What specific data do they track?",
}

# Google Sheets worksheet names
WORKSHEET_RESPONSES = "responses"

# OpenAI
OPENAI_MODEL = "gpt-4o"
OPENAI_MAX_TOKENS = 300
```

### `mcl_blueprint/models.py`

```python
"""Data models for MCL Collaborative Blueprint."""

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class AttendeeResponse:
    """A single attendee's complete response across all 3 questions.

    Attributes:
        session_id: Random unique ID per attendee session.
        timestamp: UTC timestamp of submission.
        q1_budgets: Dict mapping category name to credit allocation (sums to 100).
        q1_reasoning: Text explanation for top priority.
        q2_threat: Selected or custom threat name.
        q2_likelihood: Likelihood score (1-10).
        q2_impact: Impact score (1-10).
        q2_trigger: Text description of trigger event.
        q3_archetype: Selected archetype name.
        q3_followup: Response to conditional follow-up question.
    """

    session_id: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    # Q1
    q1_budgets: dict[str, int] = field(default_factory=dict)
    q1_reasoning: str = ""
    # Q2
    q2_threat: str = ""
    q2_likelihood: int = 5
    q2_impact: int = 5
    q2_trigger: str = ""
    # Q3
    q3_archetype: str = ""
    q3_followup: str = ""

    def to_row(self) -> list[str]:
        """Flatten to a list of strings for Google Sheets row.

        Returns:
            List of string values in column order.
        """
        budget_values = [str(self.q1_budgets.get(cat, 0)) for cat in sorted(self.q1_budgets)]
        return [
            self.session_id,
            self.timestamp,
            *budget_values,
            self.q1_reasoning,
            self.q2_threat,
            str(self.q2_likelihood),
            str(self.q2_impact),
            self.q2_trigger,
            self.q3_archetype,
            self.q3_followup,
        ]


@dataclass
class AggregatedData:
    """Aggregated data from all attendee responses for the dashboard.

    Attributes:
        total_responses: Number of submissions received.
        avg_budgets: Average credit allocation per category.
        threats: List of (threat, likelihood, impact, trigger) tuples.
        archetype_counts: Count of selections per archetype.
        top_priority: Category with highest average budget.
        top_threat: Threat with highest combined likelihood+impact.
        dominant_archetype: Archetype with most selections.
    """

    total_responses: int = 0
    avg_budgets: dict[str, float] = field(default_factory=dict)
    threats: list[tuple[str, float, float, str]] = field(default_factory=list)
    archetype_counts: dict[str, int] = field(default_factory=dict)
    top_priority: str = ""
    top_threat: str = ""
    dominant_archetype: str = ""
```

### `mcl_blueprint/sheets.py`

```python
"""Google Sheets data layer using st-gsheets-connection.

Handles reading all responses and writing new attendee submissions.
"""

import logging

import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

from mcl_blueprint.config import PRIORITY_CATEGORIES, WORKSHEET_RESPONSES

logger = logging.getLogger(__name__)

# Column order in the Google Sheet
SHEET_COLUMNS: list[str] = [
    "session_id",
    "timestamp",
    *[f"q1_{cat.lower().replace('/', '_').replace(' ', '_')}" for cat in PRIORITY_CATEGORIES],
    "q1_reasoning",
    "q2_threat",
    "q2_likelihood",
    "q2_impact",
    "q2_trigger",
    "q3_archetype",
    "q3_followup",
]


def get_connection() -> GSheetsConnection:
    """Get the cached Google Sheets connection.

    Returns:
        GSheetsConnection instance.
    """
    return st.connection("gsheets", type=GSheetsConnection)


def read_all_responses() -> pd.DataFrame:
    """Read all attendee responses from Google Sheets.

    Returns:
        DataFrame with all response rows. Empty DataFrame if no data.
    """
    conn = get_connection()
    df = conn.read(worksheet=WORKSHEET_RESPONSES, usecols=list(range(len(SHEET_COLUMNS))))
    if df is None or df.empty:
        return pd.DataFrame(columns=SHEET_COLUMNS)
    df.columns = SHEET_COLUMNS[: len(df.columns)]
    return df


def write_response(row_data: list[str]) -> None:
    """Append a single attendee response row to Google Sheets.

    Args:
        row_data: List of string values matching SHEET_COLUMNS order.
    """
    conn = get_connection()
    existing = read_all_responses()
    new_row = pd.DataFrame([row_data], columns=SHEET_COLUMNS)
    updated = pd.concat([existing, new_row], ignore_index=True)
    conn.update(worksheet=WORKSHEET_RESPONSES, data=updated)
    logger.info("Wrote response for session %s", row_data[0])
```

### `mcl_blueprint/visualizations.py`

```python
"""Plotly chart builders for the projector dashboard.

Builds three visualization types:
1. Horizontal bar chart for Q1 (Priority Budget averages)
2. Scatter plot with quadrants for Q2 (Threat Matrix)
3. Heatmap/grid for Q3 (AI Alignment Archetype counts)
"""

import plotly.express as px
import plotly.graph_objects as go

from mcl_blueprint.models import AggregatedData


def build_priority_bar_chart(data: AggregatedData) -> go.Figure:
    """Build horizontal bar chart of average budget allocations.

    Args:
        data: Aggregated response data.

    Returns:
        Plotly Figure with sorted horizontal bars.
    """
    sorted_items = sorted(data.avg_budgets.items(), key=lambda x: x[1], reverse=True)
    categories = [item[0] for item in sorted_items]
    values = [item[1] for item in sorted_items]

    fig = px.bar(
        x=values,
        y=categories,
        orientation="h",
        title="The Ideal Campus — Average Credit Allocation",
        labels={"x": "Average Credits", "y": "Category"},
        color=values,
        color_continuous_scale="Greens",
    )
    fig.update_layout(
        showlegend=False,
        coloraxis_showscale=False,
        yaxis={"categoryorder": "total ascending"},
        height=450,
        margin={"l": 150, "r": 20, "t": 60, "b": 40},
    )
    return fig


def build_threat_scatter(data: AggregatedData) -> go.Figure:
    """Build scatter plot with risk quadrants for threat data.

    Args:
        data: Aggregated response data.

    Returns:
        Plotly Figure with colored quadrant backgrounds and hover tooltips.
    """
    if not data.threats:
        fig = go.Figure()
        fig.update_layout(title="Threat Matrix — No Data Yet")
        return fig

    threats, likelihoods, impacts, triggers = zip(*data.threats)

    fig = go.Figure()

    # Quadrant backgrounds
    fig.add_shape(type="rect", x0=1, x1=5.5, y0=5.5, y1=10, fillcolor="rgba(255,165,0,0.1)", line_width=0)
    fig.add_shape(type="rect", x0=5.5, x1=10, y0=5.5, y1=10, fillcolor="rgba(255,0,0,0.15)", line_width=0)
    fig.add_shape(type="rect", x0=1, x1=5.5, y0=1, y1=5.5, fillcolor="rgba(0,128,0,0.1)", line_width=0)
    fig.add_shape(type="rect", x0=5.5, x1=10, y0=1, y1=5.5, fillcolor="rgba(255,255,0,0.1)", line_width=0)

    # Quadrant labels
    fig.add_annotation(x=8, y=9.5, text="CRITICAL CRISIS", showarrow=False, font={"size": 12, "color": "red"})
    fig.add_annotation(x=3, y=1.5, text="DISTRACTIONS", showarrow=False, font={"size": 12, "color": "green"})

    # Scatter points
    fig.add_trace(go.Scatter(
        x=list(likelihoods),
        y=list(impacts),
        mode="markers+text",
        text=list(threats),
        textposition="top center",
        hovertext=[f"Trigger: {t}" for t in triggers],
        hoverinfo="text+x+y",
        marker={"size": 14, "color": "darkblue", "opacity": 0.7},
    ))

    fig.update_layout(
        title="Threat Matrix — Constraints & Concerns",
        xaxis={"title": "Likelihood (1=Unlikely → 10=Inevitable)", "range": [0.5, 10.5]},
        yaxis={"title": "Impact (1=Annoying → 10=Existential)", "range": [0.5, 10.5]},
        height=500,
    )
    return fig


def build_archetype_grid(data: AggregatedData) -> go.Figure:
    """Build a 2x2 heatmap grid showing archetype selection counts.

    Args:
        data: Aggregated response data.

    Returns:
        Plotly Figure with highlighted dominant archetype.
    """
    archetypes = ["The Fortress", "The Ostrich", "The Lab", "The Watchtower"]
    counts = [data.archetype_counts.get(a, 0) for a in archetypes]

    # Arrange as 2x2 grid
    z = [[counts[0], counts[1]], [counts[2], counts[3]]]
    labels = [[archetypes[0], archetypes[1]], [archetypes[2], archetypes[3]]]
    text = [[f"{labels[r][c]}<br>{z[r][c]} votes" for c in range(2)] for r in range(2)]

    fig = go.Figure(data=go.Heatmap(
        z=z,
        text=text,
        texttemplate="%{text}",
        textfont={"size": 16},
        colorscale="YlGn",
        showscale=False,
    ))

    fig.update_layout(
        title=f"AI Alignment — Dominant: {data.dominant_archetype or 'N/A'}",
        xaxis={"showticklabels": False},
        yaxis={"showticklabels": False},
        height=400,
    )
    return fig
```

### `mcl_blueprint/ai_mirror.py`

```python
"""AI Mirror — OpenAI synthesis engine.

Constructs a prompt from aggregated data and generates a strategic
'Guerilla Tactic' using GPT-4o. Supports typewriter-style streaming
output via st.empty().
"""

import logging
import time

import streamlit as st
from openai import OpenAI

from mcl_blueprint.config import OPENAI_MAX_TOKENS, OPENAI_MODEL
from mcl_blueprint.models import AggregatedData

logger = logging.getLogger(__name__)


def build_synthesis_prompt(data: AggregatedData) -> str:
    """Construct the system + user prompt from aggregated data.

    Args:
        data: Aggregated response data with top_priority, top_threat,
              and dominant_archetype populated.

    Returns:
        The formatted prompt string for the OpenAI API.
    """
    return (
        "You are a strategic advisor for Muslim Campus Life. "
        f"The data shows students prioritize **{data.top_priority}** "
        f"but face **{data.top_threat}** as their top threat. "
        f"Their universities have a **{data.dominant_archetype}** "
        "policy regarding AI.\n\n"
        "**Task:** Write a specific, 3-sentence 'Guerilla Tactic' for how "
        f"these students can use AI tools to achieve {data.top_priority} "
        f"despite {data.top_threat}, taking advantage of the "
        f"{data.dominant_archetype} policy environment."
    )


def generate_synthesis(data: AggregatedData) -> str:
    """Call OpenAI API to generate the strategic synthesis.

    Args:
        data: Aggregated response data.

    Returns:
        The generated tactic text.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    prompt = build_synthesis_prompt(data)

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "You are a concise strategic advisor. Respond in exactly 3 sentences."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=OPENAI_MAX_TOKENS,
        temperature=0.8,
    )

    content = response.choices[0].message.content
    if content is None:
        raise RuntimeError("OpenAI returned empty response")
    return content


def render_typewriter(text: str, speed: float = 0.03) -> None:
    """Display text character-by-character using st.empty() for drama.

    Args:
        text: The full text to display.
        speed: Seconds between each character. Defaults to 0.03.
    """
    placeholder = st.empty()
    displayed = ""
    for char in text:
        displayed += char
        placeholder.markdown(f"### {displayed}▌")
        time.sleep(speed)
    # Final render without cursor
    placeholder.markdown(f"### {displayed}")
```

### `mcl_blueprint/components/__init__.py`

```python
"""UI components for attendee input and dashboard views."""
```

### `mcl_blueprint/components/attendee.py`

```python
"""Attendee mobile input form — wizard-style 3-step questionnaire.

Renders a mobile-optimized form using st.session_state to track
which step the user is on. Submits all data to Google Sheets at the end.
"""

import uuid

import streamlit as st

from mcl_blueprint.config import (
    ARCHETYPE_FOLLOWUPS,
    ARCHETYPES,
    IMPACT_RANGE,
    LIKELIHOOD_RANGE,
    PRIORITY_CATEGORIES,
    THREAT_OPTIONS,
    TOTAL_CREDITS,
)
from mcl_blueprint.models import AttendeeResponse
from mcl_blueprint.sheets import write_response


def render_attendee_form() -> None:
    """Render the full attendee wizard form."""
    _init_session_state()

    st.title("MCL 2026 — Your Voice Matters")
    step = st.session_state["step"]

    progress_value = step / 4  # 4 = 3 questions + thank you
    st.progress(progress_value, text=f"Step {step} of 3")

    if step == 1:
        _render_step_1_priority_budget()
    elif step == 2:
        _render_step_2_threat_matrix()
    elif step == 3:
        _render_step_3_ai_alignment()
    elif step == 4:
        _render_thank_you()


def _init_session_state() -> None:
    """Initialize session state for a new attendee."""
    if "session_id" not in st.session_state:
        st.session_state["session_id"] = str(uuid.uuid4())[:8]
    if "step" not in st.session_state:
        st.session_state["step"] = 1
    if "response" not in st.session_state:
        st.session_state["response"] = AttendeeResponse(
            session_id=st.session_state["session_id"]
        )


def _render_step_1_priority_budget() -> None:
    """Step 1: The Priority Budget — sliders summing to 100 credits."""
    st.header("Step 1: The Ideal Campus")
    st.write(f"You have **{TOTAL_CREDITS} credits** to spend on campus features. Allocate them below.")

    budgets: dict[str, int] = {}
    for category in PRIORITY_CATEGORIES:
        budgets[category] = st.slider(
            category,
            min_value=0,
            max_value=TOTAL_CREDITS,
            value=0,
            step=5,
            key=f"q1_{category}",
        )

    total = sum(budgets.values())
    remaining = TOTAL_CREDITS - total

    if remaining > 0:
        st.info(f"Credits remaining: **{remaining}**")
    elif remaining < 0:
        st.error(f"Over budget by **{abs(remaining)}** credits. Please reduce.")
    else:
        st.success("Budget balanced!")

    reasoning = st.text_area(
        "Pick your highest spend item. In one sentence, why is this more important than the others?",
        key="q1_reasoning",
    )

    if st.button("Next →", key="next_1", disabled=(total != TOTAL_CREDITS)):
        response: AttendeeResponse = st.session_state["response"]
        response.q1_budgets = budgets
        response.q1_reasoning = reasoning
        st.session_state["step"] = 2
        st.rerun()


def _render_step_2_threat_matrix() -> None:
    """Step 2: The Threat Matrix — threat selection + likelihood/impact."""
    st.header("Step 2: Constraints & Concerns")
    st.write("Identify the biggest threat to Muslim campus life.")

    threat_choice = st.selectbox(
        "Select a threat:",
        options=[*THREAT_OPTIONS, "Other"],
        key="q2_threat_select",
    )

    if threat_choice == "Other":
        threat_name = st.text_input("Describe the threat:", key="q2_threat_custom")
    else:
        threat_name = threat_choice

    likelihood = st.slider(
        "Likelihood (1 = Unlikely → 10 = Inevitable)",
        min_value=LIKELIHOOD_RANGE[0],
        max_value=LIKELIHOOD_RANGE[1],
        value=5,
        key="q2_likelihood",
    )

    impact = st.slider(
        "Impact (1 = Annoying → 10 = Existential)",
        min_value=IMPACT_RANGE[0],
        max_value=IMPACT_RANGE[1],
        value=5,
        key="q2_impact",
    )

    trigger = st.text_input(
        "What is the #1 trigger event for this threat?",
        key="q2_trigger",
    )

    if st.button("Next →", key="next_2", disabled=(not threat_name)):
        response: AttendeeResponse = st.session_state["response"]
        response.q2_threat = threat_name or ""
        response.q2_likelihood = likelihood
        response.q2_impact = impact
        response.q2_trigger = trigger
        st.session_state["step"] = 3
        st.rerun()


def _render_step_3_ai_alignment() -> None:
    """Step 3: AI Alignment Chart — archetype selection + follow-up."""
    st.header("Step 3: Institutional Policy on AI")
    st.write("Which best describes your university's stance on AI?")

    selected_archetype = ""
    for archetype, description in ARCHETYPES.items():
        if st.button(f"**{archetype}**: {description}", key=f"q3_{archetype}", use_container_width=True):
            st.session_state["q3_selected"] = archetype

    selected_archetype = st.session_state.get("q3_selected", "")

    followup_text = ""
    if selected_archetype and selected_archetype in ARCHETYPE_FOLLOWUPS:
        followup_question = ARCHETYPE_FOLLOWUPS[selected_archetype]
        followup_text = st.text_input(followup_question, key="q3_followup")

    if st.button("Submit →", key="submit_3", disabled=(not selected_archetype)):
        response: AttendeeResponse = st.session_state["response"]
        response.q3_archetype = selected_archetype
        response.q3_followup = followup_text
        write_response(response.to_row())
        st.session_state["step"] = 4
        st.rerun()


def _render_thank_you() -> None:
    """Thank you screen after submission."""
    st.balloons()
    st.header("Thank You!")
    st.write("Your response has been recorded.")
    st.write("Watch the main screen to see how your voice shapes the room's collective blueprint.")
```

### `mcl_blueprint/components/dashboard.py`

```python
"""Projector dashboard — live auto-refreshing visualization of all responses.

Displays three chart sections (one per question) plus the AI Mirror
synthesis panel. Auto-refreshes every 7 seconds to show incoming data.
"""

import logging

import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from mcl_blueprint.ai_mirror import generate_synthesis, render_typewriter
from mcl_blueprint.config import (
    ARCHETYPES,
    DASHBOARD_REFRESH_INTERVAL_MS,
    PRIORITY_CATEGORIES,
)
from mcl_blueprint.models import AggregatedData
from mcl_blueprint.sheets import read_all_responses
from mcl_blueprint.visualizations import (
    build_archetype_grid,
    build_priority_bar_chart,
    build_threat_scatter,
)

logger = logging.getLogger(__name__)


def render_dashboard() -> None:
    """Render the full projector dashboard with auto-refresh."""
    st_autorefresh(interval=DASHBOARD_REFRESH_INTERVAL_MS, key="dashboard_refresh")

    st.title("MCL 2026 — Live Collaborative Blueprint")

    df = read_all_responses()
    if df.empty:
        st.info("Waiting for responses... Share the QR code with attendees.")
        return

    data = _aggregate(df)

    st.metric("Total Responses", data.total_responses)
    st.divider()

    # Section 1: Priority Budget
    st.subheader("The Ideal Campus")
    fig_bar = build_priority_bar_chart(data)
    st.plotly_chart(fig_bar, use_container_width=True)

    st.divider()

    # Section 2: Threat Matrix
    st.subheader("Constraints & Concerns")
    fig_scatter = build_threat_scatter(data)
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.divider()

    # Section 3: AI Alignment
    st.subheader("Institutional AI Policy")
    fig_grid = build_archetype_grid(data)
    st.plotly_chart(fig_grid, use_container_width=True)

    st.divider()

    # Section 4: AI Mirror Synthesis
    st.subheader("The AI Mirror — Strategic Blueprint")
    if st.button("Generate Strategic Blueprint", type="primary", use_container_width=True):
        with st.spinner("The AI is analyzing the room's collective intelligence..."):
            tactic = generate_synthesis(data)
        render_typewriter(tactic)


def _aggregate(df: pd.DataFrame) -> AggregatedData:
    """Aggregate raw response DataFrame into dashboard-ready data.

    Args:
        df: Raw responses DataFrame from Google Sheets.

    Returns:
        AggregatedData with averages, counts, and top selections.
    """
    data = AggregatedData(total_responses=len(df))

    # Q1: Average budgets
    budget_cols = [
        f"q1_{cat.lower().replace('/', '_').replace(' ', '_')}"
        for cat in PRIORITY_CATEGORIES
    ]
    for col, cat in zip(budget_cols, PRIORITY_CATEGORIES):
        if col in df.columns:
            data.avg_budgets[cat] = pd.to_numeric(df[col], errors="coerce").mean()

    if data.avg_budgets:
        data.top_priority = max(data.avg_budgets, key=data.avg_budgets.get)

    # Q2: Threat data
    if "q2_threat" in df.columns:
        for _, row in df.iterrows():
            data.threats.append((
                str(row.get("q2_threat", "")),
                float(pd.to_numeric(row.get("q2_likelihood", 5), errors="coerce")),
                float(pd.to_numeric(row.get("q2_impact", 5), errors="coerce")),
                str(row.get("q2_trigger", "")),
            ))

        # Top threat = highest average of likelihood + impact per threat name
        threat_scores: dict[str, list[float]] = {}
        for threat, lk, imp, _ in data.threats:
            threat_scores.setdefault(threat, []).append(lk + imp)
        if threat_scores:
            data.top_threat = max(
                threat_scores,
                key=lambda t: sum(threat_scores[t]) / len(threat_scores[t]),
            )

    # Q3: Archetype counts
    if "q3_archetype" in df.columns:
        counts = df["q3_archetype"].value_counts().to_dict()
        data.archetype_counts = {k: int(v) for k, v in counts.items()}
        if data.archetype_counts:
            data.dominant_archetype = max(data.archetype_counts, key=data.archetype_counts.get)

    return data
```

### `tests/__init__.py`

```python
```

### `tests/conftest.py`

```python
"""Shared pytest fixtures for MCL Collaborative Blueprint tests."""

from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from mcl_blueprint.config import PRIORITY_CATEGORIES
from mcl_blueprint.models import AggregatedData, AttendeeResponse


@pytest.fixture
def sample_response() -> AttendeeResponse:
    """Create a sample attendee response for testing."""
    budgets = {cat: 100 // len(PRIORITY_CATEGORIES) for cat in PRIORITY_CATEGORIES}
    # Distribute remainder to first category
    budgets[PRIORITY_CATEGORIES[0]] += 100 - sum(budgets.values())

    return AttendeeResponse(
        session_id="test-abc",
        q1_budgets=budgets,
        q1_reasoning="Mental health is foundational to all other advocacy.",
        q2_threat="Budget Cuts",
        q2_likelihood=7,
        q2_impact=9,
        q2_trigger="State legislature funding review",
        q3_archetype="The Ostrich",
        q3_followup="Creates a vacuum where students have no guidance.",
    )


@pytest.fixture
def sample_aggregated_data() -> AggregatedData:
    """Create sample aggregated data for visualization tests."""
    return AggregatedData(
        total_responses=15,
        avg_budgets={
            "Mental Health": 25.0,
            "Prayer Space": 20.0,
            "Halal Food": 18.0,
            "Chaplaincy": 12.0,
            "Security/Safety": 10.0,
            "Admin Access": 8.0,
            "Legal Defense": 7.0,
        },
        threats=[
            ("Budget Cuts", 7.0, 9.0, "State funding review"),
            ("Doxxing", 6.0, 8.0, "Social media campaign"),
            ("Surveillance", 5.0, 7.0, "New campus policy"),
        ],
        archetype_counts={
            "The Ostrich": 8,
            "The Fortress": 4,
            "The Lab": 2,
            "The Watchtower": 1,
        },
        top_priority="Mental Health",
        top_threat="Budget Cuts",
        dominant_archetype="The Ostrich",
    )


@pytest.fixture
def sample_responses_df() -> pd.DataFrame:
    """Create a sample DataFrame mimicking Google Sheets data."""
    budget_cols = [
        f"q1_{cat.lower().replace('/', '_').replace(' ', '_')}"
        for cat in PRIORITY_CATEGORIES
    ]
    data = {
        "session_id": ["abc", "def", "ghi"],
        "timestamp": ["2026-02-01T10:00:00", "2026-02-01T10:01:00", "2026-02-01T10:02:00"],
        **{col: [15, 20, 10] for col in budget_cols},
        "q1_reasoning": ["reason1", "reason2", "reason3"],
        "q2_threat": ["Budget Cuts", "Doxxing", "Budget Cuts"],
        "q2_likelihood": [7, 6, 8],
        "q2_impact": [9, 8, 7],
        "q2_trigger": ["trigger1", "trigger2", "trigger3"],
        "q3_archetype": ["The Ostrich", "The Fortress", "The Ostrich"],
        "q3_followup": ["followup1", "followup2", "followup3"],
    }
    return pd.DataFrame(data)


@pytest.fixture
def mock_openai() -> MagicMock:
    """Mock OpenAI client for AI Mirror tests."""
    mock = MagicMock()
    mock.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content="This is a test tactic. Sentence two. Sentence three."))
    ]
    return mock


@pytest.fixture
def mock_sheets_read(sample_responses_df: pd.DataFrame):
    """Mock Google Sheets read to return sample data."""
    with patch("mcl_blueprint.sheets.read_all_responses", return_value=sample_responses_df) as mock:
        yield mock
```

### `tests/test_config.py`

```python
"""Tests for configuration constants."""

from mcl_blueprint.config import (
    ARCHETYPE_FOLLOWUPS,
    ARCHETYPES,
    PRIORITY_CATEGORIES,
    THREAT_OPTIONS,
    TOTAL_CREDITS,
)


class TestConfig:
    """Verify configuration constants are valid."""

    def test_priority_categories_not_empty(self) -> None:
        assert len(PRIORITY_CATEGORIES) > 0

    def test_total_credits_is_100(self) -> None:
        assert TOTAL_CREDITS == 100

    def test_threat_options_not_empty(self) -> None:
        assert len(THREAT_OPTIONS) > 0

    def test_archetypes_have_descriptions(self) -> None:
        for archetype, desc in ARCHETYPES.items():
            assert archetype, "Archetype name cannot be empty"
            assert desc, f"Archetype '{archetype}' must have a description"

    def test_archetype_followups_match_archetypes(self) -> None:
        """Every archetype with a followup must exist in ARCHETYPES."""
        for archetype in ARCHETYPE_FOLLOWUPS:
            assert archetype in ARCHETYPES, f"Followup for unknown archetype: {archetype}"
```

### `tests/test_models.py`

```python
"""Tests for data models."""

from mcl_blueprint.config import PRIORITY_CATEGORIES
from mcl_blueprint.models import AggregatedData, AttendeeResponse


class TestAttendeeResponse:
    """Tests for AttendeeResponse dataclass."""

    def test_creation_with_defaults(self) -> None:
        r = AttendeeResponse(session_id="test")
        assert r.session_id == "test"
        assert r.q1_budgets == {}
        assert r.q2_likelihood == 5

    def test_to_row_produces_list(self, sample_response: AttendeeResponse) -> None:
        row = sample_response.to_row()
        assert isinstance(row, list)
        assert row[0] == "test-abc"  # session_id

    def test_to_row_length(self, sample_response: AttendeeResponse) -> None:
        row = sample_response.to_row()
        # session_id + timestamp + 7 budgets + reasoning + threat + likelihood + impact + trigger + archetype + followup
        expected_len = 2 + len(PRIORITY_CATEGORIES) + 1 + 1 + 1 + 1 + 1 + 1 + 1
        assert len(row) == expected_len


class TestAggregatedData:
    """Tests for AggregatedData dataclass."""

    def test_creation_with_defaults(self) -> None:
        data = AggregatedData()
        assert data.total_responses == 0
        assert data.avg_budgets == {}

    def test_sample_data_has_top_values(self, sample_aggregated_data: AggregatedData) -> None:
        assert sample_aggregated_data.top_priority == "Mental Health"
        assert sample_aggregated_data.top_threat == "Budget Cuts"
        assert sample_aggregated_data.dominant_archetype == "The Ostrich"
```

### `tests/test_visualizations.py`

```python
"""Tests for Plotly visualization builders."""

import plotly.graph_objects as go

from mcl_blueprint.models import AggregatedData
from mcl_blueprint.visualizations import (
    build_archetype_grid,
    build_priority_bar_chart,
    build_threat_scatter,
)


class TestPriorityBarChart:
    """Tests for the Q1 horizontal bar chart."""

    def test_returns_figure(self, sample_aggregated_data: AggregatedData) -> None:
        fig = build_priority_bar_chart(sample_aggregated_data)
        assert isinstance(fig, go.Figure)

    def test_has_data(self, sample_aggregated_data: AggregatedData) -> None:
        fig = build_priority_bar_chart(sample_aggregated_data)
        assert len(fig.data) > 0


class TestThreatScatter:
    """Tests for the Q2 scatter plot."""

    def test_returns_figure(self, sample_aggregated_data: AggregatedData) -> None:
        fig = build_threat_scatter(sample_aggregated_data)
        assert isinstance(fig, go.Figure)

    def test_empty_data_returns_figure(self) -> None:
        empty = AggregatedData()
        fig = build_threat_scatter(empty)
        assert isinstance(fig, go.Figure)

    def test_has_quadrant_shapes(self, sample_aggregated_data: AggregatedData) -> None:
        fig = build_threat_scatter(sample_aggregated_data)
        assert len(fig.layout.shapes) == 4  # 4 quadrants


class TestArchetypeGrid:
    """Tests for the Q3 heatmap grid."""

    def test_returns_figure(self, sample_aggregated_data: AggregatedData) -> None:
        fig = build_archetype_grid(sample_aggregated_data)
        assert isinstance(fig, go.Figure)

    def test_title_contains_dominant(self, sample_aggregated_data: AggregatedData) -> None:
        fig = build_archetype_grid(sample_aggregated_data)
        assert "The Ostrich" in fig.layout.title.text
```

### `tests/test_ai_mirror.py`

```python
"""Tests for the AI Mirror synthesis engine."""

from mcl_blueprint.ai_mirror import build_synthesis_prompt
from mcl_blueprint.models import AggregatedData


class TestBuildSynthesisPrompt:
    """Tests for prompt construction."""

    def test_includes_top_priority(self, sample_aggregated_data: AggregatedData) -> None:
        prompt = build_synthesis_prompt(sample_aggregated_data)
        assert "Mental Health" in prompt

    def test_includes_top_threat(self, sample_aggregated_data: AggregatedData) -> None:
        prompt = build_synthesis_prompt(sample_aggregated_data)
        assert "Budget Cuts" in prompt

    def test_includes_dominant_archetype(self, sample_aggregated_data: AggregatedData) -> None:
        prompt = build_synthesis_prompt(sample_aggregated_data)
        assert "The Ostrich" in prompt

    def test_includes_task_instruction(self, sample_aggregated_data: AggregatedData) -> None:
        prompt = build_synthesis_prompt(sample_aggregated_data)
        assert "Guerilla Tactic" in prompt
```

---

## API Design

### External API: OpenAI Chat Completions

**Endpoint**: `https://api.openai.com/v1/chat/completions`

**Request**:
```json
{
  "model": "gpt-4o",
  "messages": [
    {
      "role": "system",
      "content": "You are a concise strategic advisor. Respond in exactly 3 sentences."
    },
    {
      "role": "user",
      "content": "You are a strategic advisor for Muslim Campus Life. The data shows students prioritize Mental Health but face Budget Cuts. Their universities have a The Ostrich policy regarding AI. Task: Write a 3-sentence Guerilla Tactic..."
    }
  ],
  "max_tokens": 300,
  "temperature": 0.8
}
```

**Response** (success):
```json
{
  "choices": [
    {
      "message": {
        "content": "Deploy a free AI chatbot trained on mental health resources..."
      }
    }
  ]
}
```

### External API: Google Sheets (via st-gsheets-connection)

**Sheet Structure** — Single worksheet named `responses`:

| Column | Type | Description |
|--------|------|-------------|
| `session_id` | string | UUID-8 per attendee |
| `timestamp` | string | ISO 8601 UTC timestamp |
| `q1_chaplaincy` | int | Credits allocated (0-100) |
| `q1_prayer_space` | int | Credits allocated (0-100) |
| `q1_halal_food` | int | Credits allocated (0-100) |
| `q1_mental_health` | int | Credits allocated (0-100) |
| `q1_admin_access` | int | Credits allocated (0-100) |
| `q1_security_safety` | int | Credits allocated (0-100) |
| `q1_legal_defense` | int | Credits allocated (0-100) |
| `q1_reasoning` | string | Free text explanation |
| `q2_threat` | string | Selected or custom threat |
| `q2_likelihood` | int | 1-10 scale |
| `q2_impact` | int | 1-10 scale |
| `q2_trigger` | string | Free text trigger event |
| `q3_archetype` | string | One of 4 archetype names |
| `q3_followup` | string | Answer to conditional question |

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                       ATTENDEES (Mobile)                            │
│              mcl-app.streamlit.app  (QR Code)                       │
│                                                                     │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    │
│   │  Step 1   │───▶│  Step 2   │───▶│  Step 3   │───▶│ Thank You│    │
│   │ Priority  │    │  Threat   │    │    AI     │    │  Screen  │    │
│   │  Budget   │    │  Matrix   │    │ Alignment │    │          │    │
│   └──────────┘    └──────────┘    └──────────┘    └─────┬────┘    │
│                                                          │          │
└──────────────────────────────────────────────────────────┼──────────┘
                                                           │
                                                    write_response()
                                                           │
                                                           ▼
                                              ┌────────────────────┐
                                              │   Google Sheets    │
                                              │   (Single Sheet)   │
                                              │  "responses" tab   │
                                              └────────┬───────────┘
                                                       │
                                                read_all_responses()
                                                       │
                                                       ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   PROJECTOR DASHBOARD                                │
│        mcl-app.streamlit.app/?mode=admin_dashboard                  │
│        Auto-refreshes every 7 seconds                               │
│                                                                     │
│   ┌──────────────────┐  ┌──────────────────┐  ┌────────────────┐  │
│   │  Q1: Bar Chart   │  │  Q2: Scatter Plot │  │ Q3: Heatmap   │  │
│   │  (Avg Budgets)   │  │  (Threat Matrix)  │  │ (Archetypes)  │  │
│   └──────────────────┘  └──────────────────┘  └────────────────┘  │
│                                                                     │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │             AI MIRROR — Generate Strategic Blueprint          │  │
│   │  [Button] ──▶ OpenAI GPT-4o ──▶ Typewriter Display          │  │
│   └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Security Considerations

1. **API Key Protection**
   - OpenAI API key stored in `st.secrets["OPENAI_API_KEY"]` — never in code
   - Google Sheets service account credentials in `st.secrets["connections.gsheets"]`
   - `.streamlit/secrets.toml` is in `.gitignore` — never committed
   - Streamlit Community Cloud stores secrets encrypted

2. **Input Validation**
   - Budget sliders constrained to 0-100 range by Streamlit widgets
   - Budget total enforced to sum to exactly 100 before submission
   - Likelihood/Impact sliders constrained to 1-10
   - Free text inputs limited to reasonable lengths by Streamlit defaults
   - Dropdown selections validated against known options

3. **Dashboard Access**
   - Dashboard accessible only via `?mode=admin_dashboard` query parameter
   - Security-by-obscurity approach — acceptable for a 45-person internal conference
   - No attendee data is individually identifiable (random session IDs)

4. **Error Handling**
   - OpenAI API failures caught and displayed as user-friendly messages
   - Google Sheets connection failures show "waiting for data" state
   - No sensitive data in error messages

---

## Performance Considerations

1. **Google Sheets API Limits**
   - 60 writes/min/user — sufficient for 45 users submitting once
   - Dashboard reads on 7-second interval — well within read limits
   - `st-gsheets-connection` handles caching automatically

2. **Dashboard Refresh**
   - `streamlit_autorefresh` polls at 7-second intervals
   - Full DataFrame re-read each cycle — acceptable for <50 rows
   - Plotly charts rendered client-side for minimal server load

3. **OpenAI API**
   - Synthesis is on-demand (button press), not automatic
   - Single API call per button press — no rate limit concerns
   - `max_tokens=300` keeps response fast and focused

4. **Mobile Performance**
   - Centered layout with minimal widgets per step
   - No heavy JavaScript or custom components
   - Progressive wizard avoids loading all questions at once
