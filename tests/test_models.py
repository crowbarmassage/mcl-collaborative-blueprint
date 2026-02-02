"""Tests for data models."""

from mcl_blueprint.config import PRIORITY_CATEGORIES
from mcl_blueprint.models import AggregatedData, AttendeeResponse


class TestAttendeeResponse:
    """Tests for AttendeeResponse dataclass."""

    def test_creation_with_defaults(self) -> None:
        r = AttendeeResponse(session_id="test")
        assert r.session_id == "test"
        assert r.q1_budgets == {}
        assert r.q2_likelihood == 5

    def test_to_row_produces_list(self, sample_response: AttendeeResponse) -> None:
        row = sample_response.to_row()
        assert isinstance(row, list)
        assert row[0] == "test-abc"  # session_id

    def test_to_row_length(self, sample_response: AttendeeResponse) -> None:
        row = sample_response.to_row()
        # session_id + timestamp + 7 budgets + reasoning
        # + threat + likelihood + impact + trigger + archetype + followup
        expected_len = 2 + len(PRIORITY_CATEGORIES) + 1 + 1 + 1 + 1 + 1 + 1 + 1
        assert len(row) == expected_len


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
