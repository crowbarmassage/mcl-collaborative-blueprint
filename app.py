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
