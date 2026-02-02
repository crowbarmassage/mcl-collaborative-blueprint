"""Integration tests for MCL Collaborative Blueprint.

Tests the full data flow from attendee response to dashboard aggregation.
All external dependencies (Google Sheets, OpenAI) are mocked.
"""

from mcl_blueprint.ai_mirror import build_synthesis_prompt
from mcl_blueprint.models import AggregatedData, AttendeeResponse
from mcl_blueprint.sheets import SHEET_COLUMNS


class TestEndToEndFlow:
    """Test the complete data pipeline."""

    def test_response_to_row_matches_sheet_columns(
        self, sample_response: AttendeeResponse
    ) -> None:
        """Verify AttendeeResponse.to_row() produces correct column count."""
        row = sample_response.to_row()
        assert len(row) == len(SHEET_COLUMNS)

    def test_aggregation_produces_synthesis_inputs(
        self, sample_aggregated_data: AggregatedData
    ) -> None:
        """Verify aggregation provides all data needed for AI synthesis."""
        assert sample_aggregated_data.top_priority != ""
        assert sample_aggregated_data.top_threat != ""
        assert sample_aggregated_data.dominant_archetype != ""

    def test_full_pipeline_prompt_is_valid(
        self, sample_aggregated_data: AggregatedData
    ) -> None:
        """Verify the synthesis prompt is well-formed from aggregated data."""
        prompt = build_synthesis_prompt(sample_aggregated_data)
        assert len(prompt) > 50
        assert "Guerilla Tactic" in prompt
