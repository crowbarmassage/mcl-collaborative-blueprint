"""Projector dashboard — live auto-refreshing visualization of all responses.

Displays three chart sections (one per question) plus the AI Mirror
synthesis panel. Auto-refreshes every 7 seconds to show incoming data.
"""

import logging

import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from mcl_blueprint.ai_mirror import generate_synthesis
from mcl_blueprint.config import (
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
    """Render the full projector dashboard with auto-refresh.

    Uses on_click callbacks + a three-phase flow for AI generation:
    1. Button on_click callback sets a flag (reliable even during autorefresh)
    2. On rerun, autorefresh is skipped and the API call runs uninterrupted
    3. Result is stored and st.rerun() triggers the display phase with typewriter
    """
    should_generate = st.session_state.pop("ai_should_generate", False)
    has_result = "ai_tactic" in st.session_state

    # Only auto-refresh when idle (not generating, no result displayed)
    if not should_generate and not has_result:
        st_autorefresh(
            interval=DASHBOARD_REFRESH_INTERVAL_MS, key="dashboard_refresh"
        )

    st.title("MCL 2026 — Live Collaborative Blueprint")

    df = read_all_responses()
    if df.empty:
        st.info("Waiting for responses... Share the QR code with attendees.")
        return

    data = aggregate(df)

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

    if has_result:
        tactic = st.session_state["ai_tactic"]
        st.markdown(f"### {tactic}")
        _render_synthesis_buttons()
    elif should_generate:
        # Phase 2: autorefresh is OFF, call API then rerun into display phase
        with st.spinner(
            "The AI is analyzing the room's collective intelligence..."
        ):
            tactic = generate_synthesis(data)
        st.session_state["ai_tactic"] = tactic
        st.rerun()
    else:
        st.button(
            "Generate Strategic Blueprint",
            type="primary",
            use_container_width=True,
            on_click=_on_generate_click,
        )


def _on_generate_click() -> None:
    """Callback for Generate button — sets flag before rerun."""
    st.session_state["ai_should_generate"] = True


def _on_regenerate_click() -> None:
    """Callback for Regenerate button — clears result and sets flag."""
    st.session_state.pop("ai_tactic", None)
    st.session_state["ai_should_generate"] = True


def _on_resume_click() -> None:
    """Callback for Resume button — clears result to re-enable autorefresh."""
    st.session_state.pop("ai_tactic", None)


def _render_synthesis_buttons() -> None:
    """Show Regenerate and Resume Live Updates buttons."""
    col1, col2 = st.columns(2)
    with col1:
        st.button(
            "Regenerate",
            key="btn_regen",
            use_container_width=True,
            on_click=_on_regenerate_click,
        )
    with col2:
        st.button(
            "Resume Live Updates",
            key="btn_resume",
            use_container_width=True,
            on_click=_on_resume_click,
        )


def aggregate(df: pd.DataFrame) -> AggregatedData:
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
    for col, cat in zip(budget_cols, PRIORITY_CATEGORIES, strict=True):
        if col in df.columns:
            data.avg_budgets[cat] = float(
                pd.to_numeric(df[col], errors="coerce").mean()
            )

    if data.avg_budgets:
        data.top_priority = max(data.avg_budgets, key=data.avg_budgets.get)  # type: ignore[arg-type]

    # Q2: Threat data
    if "q2_threat" in df.columns:
        for _, row in df.iterrows():
            data.threats.append(
                (
                    str(row.get("q2_threat", "")),
                    float(pd.to_numeric(row.get("q2_likelihood", 5), errors="coerce")),
                    float(pd.to_numeric(row.get("q2_impact", 5), errors="coerce")),
                    str(row.get("q2_trigger", "")),
                )
            )

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
            data.dominant_archetype = max(
                data.archetype_counts,
                key=data.archetype_counts.get,  # type: ignore[arg-type]
            )

    return data
