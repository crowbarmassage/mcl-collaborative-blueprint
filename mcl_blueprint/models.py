"""Data models for MCL Collaborative Blueprint."""

from dataclasses import dataclass, field
from datetime import UTC, datetime

from mcl_blueprint.config import PRIORITY_CATEGORIES


@dataclass
class AttendeeResponse:
    """A single attendee's complete response across all 3 questions.

    Attributes:
        session_id: Random unique ID per attendee session.
        timestamp: UTC timestamp of submission.
        q1_budgets: Dict mapping category name to credit allocation (sums to 100).
        q1_reasoning: Text explanation for top priority.
        q2_threat: Selected or custom threat name.
        q2_likelihood: Likelihood score (1-10).
        q2_impact: Impact score (1-10).
        q2_trigger: Text description of trigger event.
        q3_archetype: Selected archetype name.
        q3_followup: Response to conditional follow-up question.
    """

    session_id: str
    user_id: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    # Q1
    q1_budgets: dict[str, int] = field(default_factory=dict)
    q1_reasoning: str = ""
    q1_other_description: str = ""
    # Q2
    q2_threat: str = ""
    q2_likelihood: int = 5
    q2_impact: int = 5
    q2_trigger: str = ""
    # Q3
    q3_archetype: str = ""
    q3_followup: str = ""

    def to_row(self) -> list[str]:
        """Flatten to a list of strings for Google Sheets row.

        Returns:
            List of string values in column order matching SHEET_COLUMNS.
        """
        budget_values = [
            str(self.q1_budgets.get(cat, 0)) for cat in PRIORITY_CATEGORIES
        ]
        return [
            self.session_id,
            self.user_id,
            self.timestamp,
            *budget_values,
            self.q1_other_description,
            self.q1_reasoning,
            self.q2_threat,
            str(self.q2_likelihood),
            str(self.q2_impact),
            self.q2_trigger,
            self.q3_archetype,
            self.q3_followup,
        ]


@dataclass
class Registration:
    """A single attendee registration record.

    Attributes:
        user_id: 4-digit unique identifier chosen by attendee.
        passcode: 4-digit passcode for login.
        timestamp: UTC timestamp of registration.
        job_title: Optional job title.
        school_name: Name of school/university.
        university_type: Type of institution.
        locale: Urban/Suburban/Rural.
        role: Attendee's role.
        region: Geographic region.
        suggested_question: Optional question suggestion.
    """

    user_id: str
    passcode: str
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    job_title: str = ""
    school_name: str = ""
    university_type: str = ""
    locale: str = ""
    role: str = ""
    region: str = ""
    suggested_question: str = ""

    def to_row(self) -> list[str]:
        """Flatten to a list of strings for Google Sheets row.

        Returns:
            List of string values in registration column order.
        """
        return [
            self.user_id,
            self.passcode,
            self.timestamp,
            self.job_title,
            self.school_name,
            self.university_type,
            self.locale,
            self.role,
            self.region,
            self.suggested_question,
        ]


@dataclass
class AggregatedData:
    """Aggregated data from all attendee responses for the dashboard.

    Attributes:
        total_responses: Number of submissions received.
        avg_budgets: Average credit allocation per category.
        threats: List of (threat, likelihood, impact, trigger) tuples.
        archetype_counts: Count of selections per archetype.
        top_priority: Category with highest average budget.
        top_threat: Threat with highest combined likelihood+impact.
        dominant_archetype: Archetype with most selections.
    """

    total_responses: int = 0
    avg_budgets: dict[str, float] = field(default_factory=dict)
    threats: list[tuple[str, float, float, str]] = field(default_factory=list)
    archetype_counts: dict[str, int] = field(default_factory=dict)
    top_priority: str = ""
    top_threat: str = ""
    dominant_archetype: str = ""
