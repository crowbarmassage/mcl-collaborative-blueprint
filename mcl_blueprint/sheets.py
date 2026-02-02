"""Google Sheets data layer using st-gsheets-connection.

Handles reading all responses and writing new attendee submissions.
"""

import logging

import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

from mcl_blueprint.config import (
    PRIORITY_CATEGORIES,
    WORKSHEET_REGISTRATIONS,
    WORKSHEET_RESPONSES,
)

logger = logging.getLogger(__name__)

# Column order in the Google Sheet
SHEET_COLUMNS: list[str] = [
    "session_id",
    "user_id",
    "timestamp",
    *[
        f"q1_{cat.lower().replace('/', '_').replace(' ', '_')}"
        for cat in PRIORITY_CATEGORIES
    ],
    "q1_other_description",
    "q1_reasoning",
    "q2_threat",
    "q2_likelihood",
    "q2_impact",
    "q2_trigger",
    "q3_archetype",
    "q3_followup",
]

# Column order for registrations worksheet
REGISTRATION_COLUMNS: list[str] = [
    "user_id",
    "passcode",
    "timestamp",
    "job_title",
    "school_name",
    "university_type",
    "locale",
    "role",
    "region",
    "suggested_question",
]


def _spreadsheet_url() -> str:
    """Get the spreadsheet URL from Streamlit secrets."""
    # st.secrets parses TOML [connections.gsheets] differently across environments.
    # Walk possible paths and fall back to the connection's built-in attribute.
    try:
        return str(st.secrets["connections"]["gsheets"]["spreadsheet"])
    except (KeyError, TypeError):
        pass
    try:
        return str(st.secrets["connections.gsheets"]["spreadsheet"])
    except (KeyError, TypeError):
        pass
    # Last resort: read from the connection object itself
    conn = get_connection()
    return str(conn._instance.spreadsheet)  # type: ignore[union-attr]


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
    url = _spreadsheet_url()
    df = conn.read(
        spreadsheet=url,
        worksheet=WORKSHEET_RESPONSES,
        usecols=list(range(len(SHEET_COLUMNS))),
        ttl=5,
    )
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
    url = _spreadsheet_url()
    existing = read_all_responses()
    new_row = pd.DataFrame([row_data], columns=SHEET_COLUMNS)
    updated = pd.concat([existing, new_row], ignore_index=True)
    conn.update(spreadsheet=url, worksheet=WORKSHEET_RESPONSES, data=updated)
    logger.info("Wrote response for session %s", row_data[0])


def read_all_registrations() -> pd.DataFrame:
    """Read all registrations from Google Sheets.

    Returns:
        DataFrame with all registration rows. Empty DataFrame if no data.
    """
    conn = get_connection()
    url = _spreadsheet_url()
    df = conn.read(
        spreadsheet=url,
        worksheet=WORKSHEET_REGISTRATIONS,
        usecols=list(range(len(REGISTRATION_COLUMNS))),
        ttl=5,
    )
    if df is None or df.empty:
        return pd.DataFrame(columns=REGISTRATION_COLUMNS)
    df.columns = REGISTRATION_COLUMNS[: len(df.columns)]
    return df


def write_registration(row_data: list[str]) -> None:
    """Append a single registration row to Google Sheets.

    Args:
        row_data: List of string values matching REGISTRATION_COLUMNS order.
    """
    conn = get_connection()
    url = _spreadsheet_url()
    existing = read_all_registrations()
    new_row = pd.DataFrame([row_data], columns=REGISTRATION_COLUMNS)
    updated = pd.concat([existing, new_row], ignore_index=True)
    conn.update(spreadsheet=url, worksheet=WORKSHEET_REGISTRATIONS, data=updated)
    logger.info("Wrote registration for user %s", row_data[0])


def _col_as_str(series: pd.Series) -> pd.Series:  # type: ignore[type-arg]
    """Convert a column to clean strings, stripping '.0' from float-read values."""
    return series.astype(str).str.replace(r"\.0$", "", regex=True)


def validate_user_id_unique(user_id: str) -> bool:
    """Check if a user ID is not already taken.

    Args:
        user_id: The 4-digit user ID to check.

    Returns:
        True if the ID is available (not taken), False if already in use.
    """
    df = read_all_registrations()
    if df.empty:
        return True
    return user_id not in _col_as_str(df["user_id"]).values


def authenticate_user(user_id: str, passcode: str) -> bool:
    """Validate user credentials against the registrations sheet.

    Args:
        user_id: The 4-digit user ID.
        passcode: The 4-digit passcode.

    Returns:
        True if credentials match a registration record.
    """
    df = read_all_registrations()
    if df.empty:
        return False
    match = df[
        (_col_as_str(df["user_id"]) == user_id)
        & (_col_as_str(df["passcode"]) == passcode)
    ]
    return len(match) > 0
