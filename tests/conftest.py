"""Shared pytest fixtures for MCL Collaborative Blueprint tests."""

from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from mcl_blueprint.config import PRIORITY_CATEGORIES
from mcl_blueprint.models import AggregatedData, AttendeeResponse


@pytest.fixture
def sample_response() -> AttendeeResponse:
    """Create a sample attendee response for testing."""
    budgets = {cat: 100 // len(PRIORITY_CATEGORIES) for cat in PRIORITY_CATEGORIES}
    # Distribute remainder to first category
    budgets[PRIORITY_CATEGORIES[0]] += 100 - sum(budgets.values())

    return AttendeeResponse(
        session_id="test-abc",
        q1_budgets=budgets,
        q1_reasoning="Mental health is foundational to all other advocacy.",
        q2_threat="Budget Cuts",
        q2_likelihood=7,
        q2_impact=9,
        q2_trigger="State legislature funding review",
        q3_archetype="The Ostrich",
        q3_followup="Creates a vacuum where students have no guidance.",
    )


@pytest.fixture
def sample_aggregated_data() -> AggregatedData:
    """Create sample aggregated data for visualization tests."""
    return AggregatedData(
        total_responses=15,
        avg_budgets={
            "Mental Health": 25.0,
            "Prayer Space": 20.0,
            "Halal Food": 18.0,
            "Chaplaincy": 12.0,
            "Security/Safety": 10.0,
            "Admin Access": 8.0,
            "Legal Defense": 7.0,
        },
        threats=[
            ("Budget Cuts", 7.0, 9.0, "State funding review"),
            ("Doxxing", 6.0, 8.0, "Social media campaign"),
            ("Surveillance", 5.0, 7.0, "New campus policy"),
        ],
        archetype_counts={
            "The Ostrich": 8,
            "The Fortress": 4,
            "The Lab": 2,
            "The Watchtower": 1,
        },
        top_priority="Mental Health",
        top_threat="Budget Cuts",
        dominant_archetype="The Ostrich",
    )


@pytest.fixture
def sample_responses_df() -> pd.DataFrame:
    """Create a sample DataFrame mimicking Google Sheets data."""
    budget_cols = [
        f"q1_{cat.lower().replace('/', '_').replace(' ', '_')}"
        for cat in PRIORITY_CATEGORIES
    ]
    data: dict[str, list[str] | list[int]] = {
        "session_id": ["abc", "def", "ghi"],
        "timestamp": [
            "2026-02-01T10:00:00",
            "2026-02-01T10:01:00",
            "2026-02-01T10:02:00",
        ],
        **{col: [15, 20, 10] for col in budget_cols},
        "q1_reasoning": ["reason1", "reason2", "reason3"],
        "q2_threat": ["Budget Cuts", "Doxxing", "Budget Cuts"],
        "q2_likelihood": [7, 6, 8],
        "q2_impact": [9, 8, 7],
        "q2_trigger": ["trigger1", "trigger2", "trigger3"],
        "q3_archetype": ["The Ostrich", "The Fortress", "The Ostrich"],
        "q3_followup": ["followup1", "followup2", "followup3"],
    }
    return pd.DataFrame(data)


@pytest.fixture
def mock_openai() -> MagicMock:
    """Mock OpenAI client for AI Mirror tests."""
    mock = MagicMock()
    mock.chat.completions.create.return_value.choices = [
        MagicMock(
            message=MagicMock(
                content="This is a test tactic. Sentence two. Sentence three."
            )
        )
    ]
    return mock


@pytest.fixture
def mock_sheets_read(sample_responses_df: pd.DataFrame):  # type: ignore[no-untyped-def]
    """Mock Google Sheets read to return sample data."""
    with patch(
        "mcl_blueprint.sheets.read_all_responses",
        return_value=sample_responses_df,
    ) as mock:
        yield mock
