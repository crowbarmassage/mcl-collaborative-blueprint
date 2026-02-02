"""Registration form — new attendee sign-up with optional profile fields."""

import streamlit as st

from mcl_blueprint.config import (
    LOCALE_TYPES,
    REGION_OPTIONS,
    ROLE_OPTIONS,
    UNIVERSITY_TYPES,
)
from mcl_blueprint.models import Registration
from mcl_blueprint.sheets import validate_user_id_unique, write_registration


def render_registration_form() -> None:
    """Render the registration form with ID, passcode, and optional profile."""
    st.header("Register")
    st.write("Create your 4-digit ID and passcode to get started.")

    with st.form("registration_form"):
        user_id = st.text_input(
            "Choose a 4-digit ID (e.g. 1234)",
            max_chars=4,
            key="reg_user_id",
        )

        st.divider()
        st.subheader("Optional Profile")
        st.caption("Help us understand who's in the room.")

        job_title = st.text_input("Job Title", key="reg_job_title")
        school_name = st.text_input("School Name", key="reg_school")
        university_type = st.selectbox(
            "University Type",
            options=[""] + UNIVERSITY_TYPES,
            key="reg_uni_type",
        )
        locale = st.selectbox(
            "Campus Locale",
            options=[""] + LOCALE_TYPES,
            key="reg_locale",
        )
        role = st.selectbox(
            "Your Role",
            options=[""] + ROLE_OPTIONS,
            key="reg_role",
        )
        region = st.selectbox(
            "Region",
            options=[""] + REGION_OPTIONS,
            key="reg_region",
        )

        st.divider()
        suggested_question = st.text_area(
            "Suggest a question for the session (optional)",
            key="reg_question",
        )

        st.divider()
        passcode = st.text_input(
            "Choose a 4-digit passcode",
            max_chars=4,
            type="password",
            key="reg_passcode",
        )

        submitted = st.form_submit_button("Register", type="primary")

    if submitted:
        _handle_registration(
            user_id=user_id,
            passcode=passcode,
            job_title=job_title,
            school_name=school_name,
            university_type=str(university_type) if university_type else "",
            locale=str(locale) if locale else "",
            role=str(role) if role else "",
            region=str(region) if region else "",
            suggested_question=suggested_question,
        )


def _handle_registration(
    *,
    user_id: str,
    passcode: str,
    job_title: str,
    school_name: str,
    university_type: str,
    locale: str,
    role: str,
    region: str,
    suggested_question: str,
) -> None:
    """Validate and write registration, then auto-login."""
    if not user_id.isdigit() or len(user_id) != 4 or user_id[0] == "0":
        st.error("ID must be exactly 4 digits (1000–9999).")
        return

    if not passcode.isdigit() or len(passcode) != 4 or passcode[0] == "0":
        st.error("Passcode must be exactly 4 digits (1000–9999).")
        return

    if not validate_user_id_unique(user_id):
        st.error("This ID is already taken. Please choose a different one.")
        return

    reg = Registration(
        user_id=user_id,
        passcode=passcode,
        job_title=job_title,
        school_name=school_name,
        university_type=university_type,
        locale=locale,
        role=role,
        region=region,
        suggested_question=suggested_question,
    )
    write_registration(reg.to_row())

    st.success(
        "Registration successful! Switch to the **Log In** tab to sign in."
    )
