"""Tests for data models."""

from mcl_blueprint.config import PRIORITY_CATEGORIES
from mcl_blueprint.models import AggregatedData, AttendeeResponse, Registration
from mcl_blueprint.sheets import SHEET_COLUMNS


class TestAttendeeResponse:
    """Tests for AttendeeResponse dataclass."""

    def test_creation_with_defaults(self) -> None:
        r = AttendeeResponse(session_id="test")
        assert r.session_id == "test"
        assert r.q1_budgets == {}
        assert r.q2_likelihood == 5
        assert r.q1_other_description == ""

    def test_to_row_produces_list(self, sample_response: AttendeeResponse) -> None:
        row = sample_response.to_row()
        assert isinstance(row, list)
        assert row[0] == "test-abc"  # session_id
        assert row[1] == "1234"  # user_id

    def test_to_row_length(self, sample_response: AttendeeResponse) -> None:
        row = sample_response.to_row()
        # session_id + timestamp + 8 budgets + other_description + reasoning
        # + threat + likelihood + impact + trigger + archetype + followup = 19
        expected_len = len(SHEET_COLUMNS)
        assert len(row) == expected_len

    def test_to_row_uses_priority_categories_order(self) -> None:
        """Verify budget values follow PRIORITY_CATEGORIES order, not alphabetical."""
        budgets = {cat: i * 10 for i, cat in enumerate(PRIORITY_CATEGORIES)}
        r = AttendeeResponse(session_id="order-test", q1_budgets=budgets)
        row = r.to_row()
        # Budget values start at index 3 (after session_id, user_id, timestamp)
        for i, cat in enumerate(PRIORITY_CATEGORIES):
            assert row[3 + i] == str(i * 10), (
                f"Budget for {cat} at index {3 + i} should be {i * 10}"
            )


class TestRegistration:
    """Tests for Registration dataclass."""

    def test_creation_with_defaults(self) -> None:
        r = Registration(user_id="1234", passcode="5678")
        assert r.user_id == "1234"
        assert r.passcode == "5678"
        assert r.job_title == ""
        assert r.school_name == ""

    def test_to_row_produces_list(self, sample_registration: Registration) -> None:
        row = sample_registration.to_row()
        assert isinstance(row, list)
        assert row[0] == "1234"  # user_id
        assert row[1] == "5678"  # passcode

    def test_to_row_length(self, sample_registration: Registration) -> None:
        row = sample_registration.to_row()
        assert len(row) == 10  # 10 registration columns

    def test_to_row_field_order(self, sample_registration: Registration) -> None:
        row = sample_registration.to_row()
        assert row[0] == "1234"
        assert row[1] == "5678"
        # index 2 is timestamp
        assert row[3] == "President"  # job_title
        assert row[4] == "State University"
        assert row[5] == "Public 4-year"
        assert row[6] == "Urban"
        assert row[7] == "MSA Board Member"
        assert row[8] == "Northeast"
        assert row[9] == "How can MSAs collaborate across campuses?"


class TestAggregatedData:
    """Tests for AggregatedData dataclass."""

    def test_creation_with_defaults(self) -> None:
        data = AggregatedData()
        assert data.total_responses == 0
        assert data.avg_budgets == {}

    def test_sample_data_has_top_values(
        self, sample_aggregated_data: AggregatedData
    ) -> None:
        assert sample_aggregated_data.top_priority == "Mental Health"
        assert sample_aggregated_data.top_threat == "Budget Cuts"
        assert sample_aggregated_data.dominant_archetype == "The Ostrich"
