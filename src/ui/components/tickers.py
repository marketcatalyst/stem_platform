import streamlit as st


def render_cost_of_inaction_ticker(
    annual_losses_gbp: float, tenant_colour: str = "#FF3333"
):
    """
    Drives continuous behavioural modification and executive urgency via a prominent
    rolling ticker tape counting up active financial losses accumulating at the main busbar.
    """
    if annual_losses_gbp <= 0:
        return

    # Extrapolate granular multi-tiered operational loss profiles
    losses_per_week = annual_losses_gbp / 52.0
    losses_per_hour = losses_per_week / 168.0
    losses_per_second = losses_per_hour / 3600.0

    # Inject a custom CSS animations block to generate an active rolling ticker wrap
    st.markdown(
        f"""
        <style>
            .ticker-wrap {{
                width: 100%;
                overflow: hidden;
                background-color: #0F0F1A;
                padding: 10px 0;
                border: 1px solid #2D2D3F;
                border-left: 4px solid {tenant_colour};
                border-radius: 4px;
                margin-bottom: 20px;
            }}
            .ticker {{
                display: inline-block;
                white-space: nowrap;
                padding-right: 100%;
                animation: ticker-animation 25s linear infinite;
            }}
            .ticker-item {{
                display: inline-block;
                padding: 0 2rem;
                font-size: 1.1rem;
                color: #FFFFFF;
                font-family: 'Courier New', Courier, monospace;
            }}
            .ticker-highlight {{
                color: {tenant_colour};
                font-weight: bold;
            }}
            @keyframes ticker-animation {{
                0% {{ transform: translate3d(0, 0, 0); }}
                100% {{ transform: translate3d(-100%, 0, 0); }}
            }}
        </style>
        
        <div class="ticker-wrap">
            <div class="ticker">
                <div class="ticker-item">
                    ⚠️ <span class="ticker-highlight">CRITICAL SYSTEM INACTION TRACE:</span> 
                    Active financial bleed accumulating at main busbar...
                </div>
                <div class="ticker-item">
                    📉 Running Loss Accumulation Rate: 
                    <span class="ticker-highlight">£{losses_per_second:.4f}</span> per second
                </div>
                <div class="ticker-item">
                    ⏰ Hourly Capital Degradation projection: 
                    <span class="ticker-highlight">£{losses_per_hour:.2f}</span> / hr
                </div>
                <div class="ticker-item">
                    Bypass this waste by deploying the targeted 
                    <span style="color: #00FFCC; font-weight: bold;">STEM intervention model</span> immediately.
                </div>
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )
