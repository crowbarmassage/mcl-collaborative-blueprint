"""MCL Collaborative Blueprint — Main Streamlit entry point.

Routes between Attendee Input (mobile) and Admin Dashboard (projector)
based on the URL query parameter `?mode=admin_dashboard`.
Unauthenticated attendees see a landing page with Register/Login toggle.
"""

import streamlit as st

from mcl_blueprint.components.attendee import render_attendee_form
from mcl_blueprint.components.dashboard import render_dashboard
from mcl_blueprint.components.login import render_login_form
from mcl_blueprint.components.registration import render_registration_form
from mcl_blueprint.config import APP_TITLE, DASHBOARD_MODE_KEY, SESSION_USER_ID


def main() -> None:
    """Main entry point. Route based on query parameter and auth state."""
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon="🏛️",
        layout="wide" if _is_dashboard_mode() else "centered",
    )

    if _is_dashboard_mode():
        render_dashboard()
    elif SESSION_USER_ID in st.session_state:
        render_attendee_form()
    else:
        _render_landing_page()


def _is_dashboard_mode() -> bool:
    """Check if the URL contains ?mode=admin_dashboard."""
    params = st.query_params
    return params.get("mode", "") == DASHBOARD_MODE_KEY


def _render_landing_page() -> None:
    """Show the landing page with Register/Login toggle."""
    st.title(APP_TITLE)
    st.write("Welcome! Register or log in to begin the questionnaire.")

    tab_register, tab_login = st.tabs(["Register", "Log In"])

    with tab_register:
        render_registration_form()

    with tab_login:
        render_login_form()


if __name__ == "__main__":
    main()
