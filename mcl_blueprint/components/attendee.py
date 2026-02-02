"""Attendee mobile input form — wizard-style 3-step questionnaire.

Renders a mobile-optimized form using st.session_state to track
which step the user is on. Submits all data to Google Sheets at the end.
"""

import streamlit as st

from mcl_blueprint.config import (
    ARCHETYPE_FOLLOWUPS,
    ARCHETYPES,
    IMPACT_RANGE,
    LIKELIHOOD_RANGE,
    PRIORITY_CATEGORIES,
    SESSION_USER_ID,
    THREAT_OPTIONS,
    TOTAL_CREDITS,
)
from mcl_blueprint.models import AttendeeResponse
from mcl_blueprint.sheets import write_response


def render_attendee_form() -> None:
    """Render the full attendee wizard form."""
    _init_session_state()

    st.title("MCL 2026 — Your Voice Matters")
    step: int = st.session_state["step"]

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
        st.session_state["session_id"] = st.session_state.get(SESSION_USER_ID, "anon")
    if "step" not in st.session_state:
        st.session_state["step"] = 1
    if "response" not in st.session_state:
        st.session_state["response"] = AttendeeResponse(
            session_id=st.session_state["session_id"],
            user_id=st.session_state.get(SESSION_USER_ID, ""),
        )


def _render_step_1_priority_budget() -> None:
    """Step 1: The Priority Budget — sliders summing to 100 credits."""
    st.header("Step 1: The Ideal Campus")
    st.write(
        f"You have **{TOTAL_CREDITS} credits** to spend on campus features. "
        "Allocate them below."
    )

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

    other_description = ""
    if budgets.get("Other", 0) > 0:
        other_description = st.text_input(
            "What does 'Other' mean to you?",
            key="q1_other_description",
        )

    reasoning = st.text_area(
        "Pick your highest spend item. In one sentence, "
        "why is this more important than the others?",
        key="q1_reasoning",
    )

    if st.button("Next →", key="next_1", disabled=(total != TOTAL_CREDITS)):
        response: AttendeeResponse = st.session_state["response"]
        response.q1_budgets = budgets
        response.q1_other_description = other_description
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

    threat_name: str = ""
    if threat_choice == "Other":
        threat_name = st.text_input("Describe the threat:", key="q2_threat_custom")
    else:
        threat_name = str(threat_choice) if threat_choice else ""

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
        response.q2_threat = threat_name
        response.q2_likelihood = likelihood
        response.q2_impact = impact
        response.q2_trigger = trigger
        st.session_state["step"] = 3
        st.rerun()


def _render_step_3_ai_alignment() -> None:
    """Step 3: AI Alignment Chart — archetype selection + follow-up."""
    st.header("Step 3: Institutional Policy on AI")
    st.write("Which best describes your university's stance on AI?")

    for archetype, description in ARCHETYPES.items():
        if st.button(
            f"**{archetype}**: {description}",
            key=f"q3_{archetype}",
            use_container_width=True,
        ):
            st.session_state["q3_selected"] = archetype

    selected_archetype: str = st.session_state.get("q3_selected", "")

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
    """Thank you screen + results summary after submission."""
    from mcl_blueprint.components.results import render_results_summary

    render_results_summary()


def reset_questionnaire() -> None:
    """Reset session state to allow retaking the questionnaire."""
    st.session_state["step"] = 1
    st.session_state.pop("response", None)
    st.session_state.pop("q3_selected", None)
