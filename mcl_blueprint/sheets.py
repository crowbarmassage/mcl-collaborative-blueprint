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
    *[
        f"q1_{cat.lower().replace('/', '_').replace(' ', '_')}"
        for cat in PRIORITY_CATEGORIES
    ],
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
    df = conn.read(
        worksheet=WORKSHEET_RESPONSES,
        usecols=list(range(len(SHEET_COLUMNS))),
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
    existing = read_all_responses()
    new_row = pd.DataFrame([row_data], columns=SHEET_COLUMNS)
    updated = pd.concat([existing, new_row], ignore_index=True)
    conn.update(worksheet=WORKSHEET_RESPONSES, data=updated)
    logger.info("Wrote response for session %s", row_data[0])
