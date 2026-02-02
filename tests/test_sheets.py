"""Tests for Google Sheets data layer (mocked)."""

from unittest.mock import MagicMock, patch

import pandas as pd

from mcl_blueprint.sheets import (
    REGISTRATION_COLUMNS,
    SHEET_COLUMNS,
    authenticate_user,
    read_all_registrations,
    read_all_responses,
    validate_user_id_unique,
    write_registration,
    write_response,
)


class TestSheetColumns:
    """Verify sheet column definitions."""

    def test_columns_start_with_session_id(self) -> None:
        assert SHEET_COLUMNS[0] == "session_id"

    def test_columns_include_all_budget_fields(self) -> None:
        budget_cols = [
            c
            for c in SHEET_COLUMNS
            if c.startswith("q1_")
            and c not in ("q1_reasoning", "q1_other_description")
        ]
        assert len(budget_cols) == 8  # 8 priority categories including Other

    def test_columns_include_other_description(self) -> None:
        assert "q1_other_description" in SHEET_COLUMNS

    def test_columns_end_with_q3_followup(self) -> None:
        assert SHEET_COLUMNS[-1] == "q3_followup"


class TestRegistrationColumns:
    """Verify registration column definitions."""

    def test_columns_start_with_user_id(self) -> None:
        assert REGISTRATION_COLUMNS[0] == "user_id"

    def test_columns_count(self) -> None:
        assert len(REGISTRATION_COLUMNS) == 10

    def test_columns_include_passcode(self) -> None:
        assert "passcode" in REGISTRATION_COLUMNS


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


class TestReadAllRegistrations:
    """Tests for reading registrations."""

    @patch("mcl_blueprint.sheets.get_connection")
    def test_returns_dataframe(self, mock_conn: MagicMock) -> None:
        mock_conn.return_value.read.return_value = pd.DataFrame(
            columns=REGISTRATION_COLUMNS
        )
        df = read_all_registrations()
        assert isinstance(df, pd.DataFrame)

    @patch("mcl_blueprint.sheets.get_connection")
    def test_empty_returns_empty_df(self, mock_conn: MagicMock) -> None:
        mock_conn.return_value.read.return_value = pd.DataFrame()
        df = read_all_registrations()
        assert df.empty

    @patch("mcl_blueprint.sheets.get_connection")
    def test_none_returns_empty_df(self, mock_conn: MagicMock) -> None:
        mock_conn.return_value.read.return_value = None
        df = read_all_registrations()
        assert df.empty
        assert list(df.columns) == REGISTRATION_COLUMNS


class TestWriteRegistration:
    """Tests for writing registrations."""

    @patch("mcl_blueprint.sheets.read_all_registrations")
    @patch("mcl_blueprint.sheets.get_connection")
    def test_write_calls_update(
        self, mock_conn: MagicMock, mock_read: MagicMock
    ) -> None:
        mock_read.return_value = pd.DataFrame(columns=REGISTRATION_COLUMNS)
        row = ["1234", "5678"] + [""] * (len(REGISTRATION_COLUMNS) - 2)
        write_registration(row)
        mock_conn.return_value.update.assert_called_once()


class TestValidateUserIdUnique:
    """Tests for user ID uniqueness validation."""

    @patch("mcl_blueprint.sheets.read_all_registrations")
    def test_unique_id_returns_true(self, mock_read: MagicMock) -> None:
        mock_read.return_value = pd.DataFrame(
            [["9999", "1111"] + [""] * 8], columns=REGISTRATION_COLUMNS
        )
        assert validate_user_id_unique("1234") is True

    @patch("mcl_blueprint.sheets.read_all_registrations")
    def test_taken_id_returns_false(self, mock_read: MagicMock) -> None:
        mock_read.return_value = pd.DataFrame(
            [["1234", "5678"] + [""] * 8], columns=REGISTRATION_COLUMNS
        )
        assert validate_user_id_unique("1234") is False

    @patch("mcl_blueprint.sheets.read_all_registrations")
    def test_empty_sheet_returns_true(self, mock_read: MagicMock) -> None:
        mock_read.return_value = pd.DataFrame(columns=REGISTRATION_COLUMNS)
        assert validate_user_id_unique("1234") is True


class TestAuthenticateUser:
    """Tests for user authentication."""

    @patch("mcl_blueprint.sheets.read_all_registrations")
    def test_valid_credentials(self, mock_read: MagicMock) -> None:
        mock_read.return_value = pd.DataFrame(
            [["1234", "5678"] + [""] * 8], columns=REGISTRATION_COLUMNS
        )
        assert authenticate_user("1234", "5678") is True

    @patch("mcl_blueprint.sheets.read_all_registrations")
    def test_wrong_passcode(self, mock_read: MagicMock) -> None:
        mock_read.return_value = pd.DataFrame(
            [["1234", "5678"] + [""] * 8], columns=REGISTRATION_COLUMNS
        )
        assert authenticate_user("1234", "0000") is False

    @patch("mcl_blueprint.sheets.read_all_registrations")
    def test_unknown_user(self, mock_read: MagicMock) -> None:
        mock_read.return_value = pd.DataFrame(
            [["1234", "5678"] + [""] * 8], columns=REGISTRATION_COLUMNS
        )
        assert authenticate_user("9999", "5678") is False

    @patch("mcl_blueprint.sheets.read_all_registrations")
    def test_empty_sheet_returns_false(self, mock_read: MagicMock) -> None:
        mock_read.return_value = pd.DataFrame(columns=REGISTRATION_COLUMNS)
        assert authenticate_user("1234", "5678") is False
