"""Results Summary page — shown to attendees after completing the questionnaire.

Displays aggregated visualizations of all responses and suggested questions.
"""

import streamlit as st

from mcl_blueprint.components.dashboard import aggregate
from mcl_blueprint.sheets import read_all_registrations, read_all_responses
from mcl_blueprint.visualizations import (
    build_archetype_grid,
    build_priority_pie_chart,
    build_threat_scatter,
)


def render_results_summary() -> None:
    """Render the full results summary page after questionnaire completion."""
    st.balloons()
    st.header("Thank You! Here's What the Room Is Saying")

    df = read_all_responses()
    if df.empty:
        st.info("Your response was the first! Results will appear as more people participate.")
        _render_retake_button()
        return

    data = aggregate(df)

    st.metric("Total Responses So Far", data.total_responses)
    st.divider()

    # Section 1: Priority Budget — Pie chart
    st.subheader("The Ideal Campus")
    fig_pie = build_priority_pie_chart(data)
    st.plotly_chart(fig_pie, use_container_width=True)

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

    # Section 4: Suggested Questions
    _render_suggested_questions()

    st.divider()

    _render_retake_button()


def _render_suggested_questions() -> None:
    """Display non-empty suggested questions from all registrations."""
    st.subheader("Questions From the Room")

    reg_df = read_all_registrations()
    if reg_df.empty or "suggested_question" not in reg_df.columns:
        st.write("No questions suggested yet.")
        return

    questions = (
        reg_df["suggested_question"]
        .dropna()
        .astype(str)
        .str.strip()
    )
    questions = questions[questions != ""]

    if questions.empty:
        st.write("No questions suggested yet.")
        return

    for q in questions:
        st.markdown(f"- {q}")


def _render_retake_button() -> None:
    """Show a button to retake the questionnaire."""
    from mcl_blueprint.components.attendee import reset_questionnaire

    if st.button("Retake Questionnaire", type="secondary", use_container_width=True):
        reset_questionnaire()
        st.rerun()
