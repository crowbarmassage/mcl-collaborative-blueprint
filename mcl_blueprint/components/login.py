"""Login form — returning attendee authentication."""

import streamlit as st

from mcl_blueprint.config import SESSION_USER_ID
from mcl_blueprint.sheets import authenticate_user


def render_login_form() -> None:
    """Render the login form with ID and passcode fields."""
    st.header("Log In")
    st.write("Enter your 4-digit ID and passcode.")

    with st.form("login_form"):
        user_id = st.text_input(
            "Your 4-digit ID",
            max_chars=4,
            key="login_user_id",
        )
        passcode = st.text_input(
            "Your 4-digit passcode",
            max_chars=4,
            type="password",
            key="login_passcode",
        )
        submitted = st.form_submit_button("Log In", type="primary")

    if submitted:
        if not user_id or not passcode:
            st.error("Please enter both your ID and passcode.")
            return

        if authenticate_user(user_id, passcode):
            st.session_state[SESSION_USER_ID] = user_id
            st.success("Welcome back!")
            st.rerun()
        else:
            st.error("Invalid ID or passcode. Please try again.")
