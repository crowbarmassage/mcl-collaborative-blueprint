"""Tests for configuration constants."""

from mcl_blueprint.config import (
    ARCHETYPE_FOLLOWUPS,
    ARCHETYPES,
    LOCALE_TYPES,
    PRIORITY_CATEGORIES,
    REGION_OPTIONS,
    ROLE_OPTIONS,
    SESSION_USER_ID,
    THREAT_OPTIONS,
    TOTAL_CREDITS,
    UNIVERSITY_TYPES,
    WORKSHEET_REGISTRATIONS,
)


class TestConfig:
    """Verify configuration constants are valid."""

    def test_priority_categories_not_empty(self) -> None:
        assert len(PRIORITY_CATEGORIES) > 0

    def test_priority_categories_includes_other(self) -> None:
        assert "Other" in PRIORITY_CATEGORIES

    def test_priority_categories_count(self) -> None:
        assert len(PRIORITY_CATEGORIES) == 8

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

    def test_worksheet_registrations_defined(self) -> None:
        assert WORKSHEET_REGISTRATIONS == "registrations"

    def test_session_user_id_defined(self) -> None:
        assert SESSION_USER_ID == "user_id"

    def test_university_types_not_empty(self) -> None:
        assert len(UNIVERSITY_TYPES) > 0

    def test_locale_types_not_empty(self) -> None:
        assert len(LOCALE_TYPES) > 0

    def test_role_options_not_empty(self) -> None:
        assert len(ROLE_OPTIONS) > 0

    def test_region_options_not_empty(self) -> None:
        assert len(REGION_OPTIONS) > 0
