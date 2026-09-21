"""
Portfolio Reallocation & Governance Architecture Module.
Details the ₹4.0 Cr capital reallocation, 60-day milestones, and capital stop-loss rules.
"""

import pandas as pd
import plotly.express as px
import streamlit as st
import config


def render():
    st.header("4. Strategic Capital Realignment & Governance Architecture")
    st.markdown(
        "Reallocating **₹4.0 Crore** out of low-efficiency broad awareness channels (Reels, Influencers) "
        "to scale high-intent Google Search, Dynamic Retargeting, and a dedicated **Retention & CRM Engine**."
    )

    # 1. Budget Reallocation Table
    df_port = pd.DataFrame(config.PORTFOLIO_MATRIX)
    st.subheader("Budget Deployment Matrix (Flat ₹12.0 Cr Envelope)")
    st.dataframe(
        df_port.rename(
            columns={
                "channel": "Channel / Investment Vector",
                "initial_cr": "Initial Budget (Cr)",
                "revised_cr": "Revised Budget (Cr)",
                "net_cr": "Net Shift (Cr)",
                "cac": "Historic CAC (₹)",
                "share": "Historic Order Share (%)",
            }
        ),
        use_container_width=True,
    )

    # 2. Visual Budget Shift
    melted_port = df_port.melt(
        id_vars=["channel"], value_vars=["initial_cr", "revised_cr"], var_name="Allocation", value_name="Budget_Cr"
    )
    fig_shift = px.bar(
        melted_port,
        x="channel",
        y="Budget_Cr",
        color="Allocation",
        barmode="group",
        title="Initial vs Revised Budget Allocation Across Channels (₹ Cr)",
        color_discrete_sequence=["#EF553B", "#00CC96"],
    )
    fig_shift.update_layout(height=380)
    st.plotly_chart(fig_shift, use_container_width=True)

    st.markdown("---")

    # 3. Slide 6: 60-Day Recovery Target Matrix
    st.subheader("60-Day Recovery Targets vs Historical Benchmarks")
    df_gov = pd.DataFrame(config.RECOVERY_TARGETS).T.reset_index()
    df_gov.columns = ["Performance Metric", "Historical Actual", "30-Day Interim", "60-Day Target", "Steady-State SLA"]
    st.dataframe(df_gov, use_container_width=True)

    # 4. Kill Switches
    st.subheader("Firm Kill Criteria & Capital Pause Triggers")
    k1, k2 = st.columns(2)
    with k1:
        st.markdown(
            """
            1. **Channel-Level Spend Cuts:**
               - If any channel's CAC exceeds **₹600** after ₹25L spend, pause budget within 48 hours.
               - Reallocate balance to Google Search SEM or Retargeting.
            2. **Tier-1 Strategic Reassessment:**
               - If Tier-1 30-day cohort retention drops below **26%** by Day 45, freeze paid acquisition in Tier-1.
               - Shift capital to Tier-2 and Tier-3 hubs (CAC ₹420–₹510, retention 36%–42%).
            """
        )
    with k2:
        st.markdown(
            """
            3. **Operational Circuit Breakers:**
               - **OOS Trigger:** Pause local hub ads if out-of-stock rate exceeds **6%** for 3 consecutive days.
               - **Delivery Slippage:** Pause ads if average delivery time exceeds **17 minutes** for 48 hours.
            4. **Overall Campaign Stop-Loss:**
               - If blended CAC > **₹650** or Month-2 retention < **25%** by Day 60, halt all acquisition spend.
               - Redirect remaining funds to dark-store warehousing and baseline pricing.
            """
        )