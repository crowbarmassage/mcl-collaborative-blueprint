"""Plotly chart builders for the projector dashboard.

Builds three visualization types:
1. Horizontal bar chart for Q1 (Priority Budget averages)
2. Scatter plot with quadrants for Q2 (Threat Matrix)
3. Heatmap/grid for Q3 (AI Alignment Archetype counts)
"""

import plotly.express as px
import plotly.graph_objects as go

from mcl_blueprint.models import AggregatedData


def build_priority_pie_chart(data: AggregatedData) -> go.Figure:
    """Build a pie chart of average budget allocations.

    Args:
        data: Aggregated response data.

    Returns:
        Plotly Figure with pie chart slices for each category.
    """
    sorted_items = sorted(data.avg_budgets.items(), key=lambda x: x[1], reverse=True)
    categories = [item[0] for item in sorted_items]
    values = [item[1] for item in sorted_items]

    fig = px.pie(
        names=categories,
        values=values,
        title="The Ideal Campus — Budget Allocation",
        color_discrete_sequence=px.colors.sequential.Greens_r,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(height=450)
    return fig


def build_priority_bar_chart(data: AggregatedData) -> go.Figure:
    """Build horizontal bar chart of average budget allocations.

    Args:
        data: Aggregated response data.

    Returns:
        Plotly Figure with sorted horizontal bars.
    """
    sorted_items = sorted(data.avg_budgets.items(), key=lambda x: x[1], reverse=True)
    categories = [item[0] for item in sorted_items]
    values = [item[1] for item in sorted_items]

    fig = px.bar(
        x=values,
        y=categories,
        orientation="h",
        title="The Ideal Campus — Average Credit Allocation",
        labels={"x": "Average Credits", "y": "Category"},
        color=values,
        color_continuous_scale="Greens",
    )
    fig.update_layout(
        showlegend=False,
        coloraxis_showscale=False,
        yaxis={"categoryorder": "total ascending"},
        height=450,
        margin={"l": 150, "r": 20, "t": 60, "b": 40},
    )
    return fig


def build_threat_scatter(data: AggregatedData) -> go.Figure:
    """Build scatter plot with risk quadrants for threat data.

    Args:
        data: Aggregated response data.

    Returns:
        Plotly Figure with colored quadrant backgrounds and hover tooltips.
    """
    if not data.threats:
        fig = go.Figure()
        fig.update_layout(title="Threat Matrix — No Data Yet")
        return fig

    threats, likelihoods, impacts, triggers = zip(*data.threats, strict=True)

    fig = go.Figure()

    # Quadrant backgrounds
    fig.add_shape(
        type="rect",
        x0=1,
        x1=5.5,
        y0=5.5,
        y1=10,
        fillcolor="rgba(255,165,0,0.1)",
        line_width=0,
    )
    fig.add_shape(
        type="rect",
        x0=5.5,
        x1=10,
        y0=5.5,
        y1=10,
        fillcolor="rgba(255,0,0,0.15)",
        line_width=0,
    )
    fig.add_shape(
        type="rect",
        x0=1,
        x1=5.5,
        y0=1,
        y1=5.5,
        fillcolor="rgba(0,128,0,0.1)",
        line_width=0,
    )
    fig.add_shape(
        type="rect",
        x0=5.5,
        x1=10,
        y0=1,
        y1=5.5,
        fillcolor="rgba(255,255,0,0.1)",
        line_width=0,
    )

    # Quadrant labels
    fig.add_annotation(
        x=8,
        y=9.5,
        text="CRITICAL CRISIS",
        showarrow=False,
        font={"size": 12, "color": "red"},
    )
    fig.add_annotation(
        x=3,
        y=1.5,
        text="DISTRACTIONS",
        showarrow=False,
        font={"size": 12, "color": "green"},
    )

    # Scatter points
    fig.add_trace(
        go.Scatter(
            x=list(likelihoods),
            y=list(impacts),
            mode="markers+text",
            text=list(threats),
            textposition="top center",
            hovertext=[f"Trigger: {t}" for t in triggers],
            hoverinfo="text+x+y",
            marker={"size": 14, "color": "darkblue", "opacity": 0.7},
        )
    )

    fig.update_layout(
        title="Threat Matrix — Constraints & Concerns",
        xaxis={
            "title": "Likelihood (1=Unlikely → 10=Inevitable)",
            "range": [0.5, 10.5],
        },
        yaxis={
            "title": "Impact (1=Annoying → 10=Existential)",
            "range": [0.5, 10.5],
        },
        height=500,
    )
    return fig


def build_archetype_grid(data: AggregatedData) -> go.Figure:
    """Build a 2x2 heatmap grid showing archetype selection counts.

    Args:
        data: Aggregated response data.

    Returns:
        Plotly Figure with highlighted dominant archetype.
    """
    archetypes = ["The Fortress", "The Ostrich", "The Lab", "The Watchtower"]
    counts = [data.archetype_counts.get(a, 0) for a in archetypes]

    # Arrange as 2x2 grid
    z = [[counts[0], counts[1]], [counts[2], counts[3]]]
    labels = [[archetypes[0], archetypes[1]], [archetypes[2], archetypes[3]]]
    text = [[f"{labels[r][c]}<br>{z[r][c]} votes" for c in range(2)] for r in range(2)]

    fig = go.Figure(
        data=go.Heatmap(
            z=z,
            text=text,
            texttemplate="%{text}",
            textfont={"size": 16},
            colorscale="YlGn",
            showscale=False,
        )
    )

    fig.update_layout(
        title=f"AI Alignment — Dominant: {data.dominant_archetype or 'N/A'}",
        xaxis={"showticklabels": False},
        yaxis={"showticklabels": False},
        height=400,
    )
    return fig
