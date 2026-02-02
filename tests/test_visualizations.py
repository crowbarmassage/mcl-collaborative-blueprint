"""Tests for Plotly visualization builders."""

import plotly.graph_objects as go

from mcl_blueprint.models import AggregatedData
from mcl_blueprint.visualizations import (
    build_archetype_grid,
    build_priority_bar_chart,
    build_priority_pie_chart,
    build_threat_scatter,
)


class TestPriorityPieChart:
    """Tests for the Q1 pie chart."""

    def test_returns_figure(self, sample_aggregated_data: AggregatedData) -> None:
        fig = build_priority_pie_chart(sample_aggregated_data)
        assert isinstance(fig, go.Figure)

    def test_has_data(self, sample_aggregated_data: AggregatedData) -> None:
        fig = build_priority_pie_chart(sample_aggregated_data)
        assert len(fig.data) > 0

    def test_empty_data_returns_figure(self) -> None:
        empty = AggregatedData()
        fig = build_priority_pie_chart(empty)
        assert isinstance(fig, go.Figure)


class TestPriorityBarChart:
    """Tests for the Q1 horizontal bar chart."""

    def test_returns_figure(self, sample_aggregated_data: AggregatedData) -> None:
        fig = build_priority_bar_chart(sample_aggregated_data)
        assert isinstance(fig, go.Figure)

    def test_has_data(self, sample_aggregated_data: AggregatedData) -> None:
        fig = build_priority_bar_chart(sample_aggregated_data)
        assert len(fig.data) > 0


class TestThreatScatter:
    """Tests for the Q2 scatter plot."""

    def test_returns_figure(self, sample_aggregated_data: AggregatedData) -> None:
        fig = build_threat_scatter(sample_aggregated_data)
        assert isinstance(fig, go.Figure)

    def test_empty_data_returns_figure(self) -> None:
        empty = AggregatedData()
        fig = build_threat_scatter(empty)
        assert isinstance(fig, go.Figure)

    def test_has_quadrant_shapes(self, sample_aggregated_data: AggregatedData) -> None:
        fig = build_threat_scatter(sample_aggregated_data)
        assert len(fig.layout.shapes) == 4  # 4 quadrants

    def test_has_scatter_trace(self, sample_aggregated_data: AggregatedData) -> None:
        fig = build_threat_scatter(sample_aggregated_data)
        scatter_traces = [t for t in fig.data if isinstance(t, go.Scatter)]
        assert len(scatter_traces) == 1


class TestArchetypeGrid:
    """Tests for the Q3 heatmap grid."""

    def test_returns_figure(self, sample_aggregated_data: AggregatedData) -> None:
        fig = build_archetype_grid(sample_aggregated_data)
        assert isinstance(fig, go.Figure)

    def test_title_contains_dominant(
        self, sample_aggregated_data: AggregatedData
    ) -> None:
        fig = build_archetype_grid(sample_aggregated_data)
        assert "The Ostrich" in fig.layout.title.text

    def test_empty_data_shows_na(self) -> None:
        empty = AggregatedData()
        fig = build_archetype_grid(empty)
        assert "N/A" in fig.layout.title.text
