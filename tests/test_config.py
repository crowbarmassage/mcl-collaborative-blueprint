"""Tests for configuration constants."""

from mcl_blueprint.config import (
    ARCHETYPE_FOLLOWUPS,
    ARCHETYPES,
    PRIORITY_CATEGORIES,
    THREAT_OPTIONS,
    TOTAL_CREDITS,
)


class TestConfig:
    """Verify configuration constants are valid."""

    def test_priority_categories_not_empty(self) -> None:
        assert len(PRIORITY_CATEGORIES) > 0

    def test_total_credits_is_100(self) -> None:
        assert TOTAL_CREDITS == 100

    def test_threat_options_not_empty(self) -> None:
        assert len(THREAT_OPTIONS) > 0

    def test_archetypes_have_descriptions(self) -> None:
        for archetype, desc in ARCHETYPES.items():
            assert archetype, "Archetype name cannot be empty"
            assert desc, f"Archetype '{archetype}' must have a description"

    def test_archetype_followups_match_archetypes(self) -> None:
        """Every archetype with a followup must exist in ARCHETYPES."""
        for archetype in ARCHETYPE_FOLLOWUPS:
            assert archetype in ARCHETYPES, (
                f"Followup for unknown archetype: {archetype}"
            )
