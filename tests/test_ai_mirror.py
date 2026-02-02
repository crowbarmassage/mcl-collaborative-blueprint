"""Tests for the AI Mirror synthesis engine."""

from mcl_blueprint.ai_mirror import build_synthesis_prompt
from mcl_blueprint.models import AggregatedData


class TestBuildSynthesisPrompt:
    """Tests for prompt construction."""

    def test_includes_top_priority(
        self, sample_aggregated_data: AggregatedData
    ) -> None:
        prompt = build_synthesis_prompt(sample_aggregated_data)
        assert "Mental Health" in prompt

    def test_includes_top_threat(self, sample_aggregated_data: AggregatedData) -> None:
        prompt = build_synthesis_prompt(sample_aggregated_data)
        assert "Budget Cuts" in prompt

    def test_includes_dominant_archetype(
        self, sample_aggregated_data: AggregatedData
    ) -> None:
        prompt = build_synthesis_prompt(sample_aggregated_data)
        assert "The Ostrich" in prompt

    def test_includes_task_instruction(
        self, sample_aggregated_data: AggregatedData
    ) -> None:
        prompt = build_synthesis_prompt(sample_aggregated_data)
        assert "Guerilla Tactic" in prompt

    def test_prompt_is_nonempty(self, sample_aggregated_data: AggregatedData) -> None:
        prompt = build_synthesis_prompt(sample_aggregated_data)
        assert len(prompt) > 100
