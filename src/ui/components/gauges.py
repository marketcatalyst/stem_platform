import plotly.graph_objects as go


def render_efficiency_ghost_dial(
    current_efficiency_pct: float,
    optimized_ceiling_pct: float,
    dial_title: str,
    accent_colour: str = "#00FFCC",
) -> go.Figure:
    """
    Renders a high-contrast real-time current efficiency dial overlaid with a
    luminous, semi-transparent 'ghost arc' showing the optimised performance ceiling.
    """
    # Enforce strict bounds to prevent charting overflow
    curr = max(0.0, min(100.0, current_efficiency_pct))
    ceil = max(curr, min(100.0, optimized_ceiling_pct))

    fig = go.Figure()

    # 1. Base Degraded Performance Needle & Gauge Track
    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=curr,
            title={
                "text": f"<b>{dial_title}</b>",
                "font": {"size": 16, "color": "#FFFFFF"},
            },
            number={"suffix": "%", "font": {"color": "#FFFFFF", "size": 24}},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#444455"},
                "bar": {
                    "color": "#FF3333" if curr < 80 else "#FFAA00",
                    "thickness": 0.25,
                },
                "bgcolor": "#1A1A26",
                "bordercolor": "#2D2D3F",
                "borderwidth": 1,
                # 2. Layering the Glowing Semi-Transparent "Ghost Arc" Optimization Target
                "steps": [
                    {
                        "range": [curr, ceil],
                        "color": accent_colour,
                        "line": {"color": accent_colour, "width": 1},
                        # Mimics a luminous, semi-transparent overlay in Plotly specs
                        "name": "STEM Optimization Target",
                    }
                ],
            },
        )
    )

    # Apply dark, responsive ambient dashboard design constraints
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=40, b=20),
        height=220,
        font={"color": "#FFFFFF", "family": "Arial"},
    )

    return fig
