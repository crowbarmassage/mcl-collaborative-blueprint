"""Tests for Google Sheets data layer (mocked)."""

from unittest.mock import MagicMock, patch

import pandas as pd

from mcl_blueprint.sheets import SHEET_COLUMNS, read_all_responses, write_response


class TestSheetColumns:
    """Verify sheet column definitions."""

    def test_columns_start_with_session_id(self) -> None:
        assert SHEET_COLUMNS[0] == "session_id"

    def test_columns_include_all_budget_fields(self) -> None:
        budget_cols = [
            c for c in SHEET_COLUMNS if c.startswith("q1_") and c != "q1_reasoning"
        ]
        assert len(budget_cols) == 7  # 7 priority categories

    def test_columns_end_with_q3_followup(self) -> None:
        assert SHEET_COLUMNS[-1] == "q3_followup"


class TestReadAllResponses:
    """Tests for reading from Google Sheets."""

    @patch("mcl_blueprint.sheets.get_connection")
    def test_returns_dataframe(self, mock_conn: MagicMock) -> None:
        mock_conn.return_value.read.return_value = pd.DataFrame(columns=SHEET_COLUMNS)
        df = read_all_responses()
        assert isinstance(df, pd.DataFrame)

    @patch("mcl_blueprint.sheets.get_connection")
    def test_empty_sheet_returns_empty_df(self, mock_conn: MagicMock) -> None:
        mock_conn.return_value.read.return_value = pd.DataFrame()
        df = read_all_responses()
        assert df.empty

    @patch("mcl_blueprint.sheets.get_connection")
    def test_none_response_returns_empty_df(self, mock_conn: MagicMock) -> None:
        mock_conn.return_value.read.return_value = None
        df = read_all_responses()
        assert df.empty
        assert list(df.columns) == SHEET_COLUMNS


class TestWriteResponse:
    """Tests for writing to Google Sheets."""

    @patch("mcl_blueprint.sheets.read_all_responses")
    @patch("mcl_blueprint.sheets.get_connection")
    def test_write_calls_update(
        self, mock_conn: MagicMock, mock_read: MagicMock
    ) -> None:
        mock_read.return_value = pd.DataFrame(columns=SHEET_COLUMNS)
        row = ["test-id", "2026-02-01T00:00:00"] + ["0"] * (len(SHEET_COLUMNS) - 2)
        write_response(row)
        mock_conn.return_value.update.assert_called_once()

    @patch("mcl_blueprint.sheets.read_all_responses")
    @patch("mcl_blueprint.sheets.get_connection")
    def test_write_appends_to_existing(
        self, mock_conn: MagicMock, mock_read: MagicMock
    ) -> None:
        existing = pd.DataFrame(
            [["old-id"] + ["x"] * (len(SHEET_COLUMNS) - 1)],
            columns=SHEET_COLUMNS,
        )
        mock_read.return_value = existing
        new_row = ["new-id", "2026-02-01T00:00:00"] + ["0"] * (len(SHEET_COLUMNS) - 2)
        write_response(new_row)
        call_args = mock_conn.return_value.update.call_args
        updated_df = call_args.kwargs["data"]
        assert len(updated_df) == 2
