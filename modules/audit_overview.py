"""
Audit Overview Module.
Presents the executive forensic autopsy, conversion waterfall, and retention collapse.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import config


def render():
    st.header("1. Executive Diagnosis & Forensic Autopsy")
    st.markdown(
        "Mathematical invalidation of demand and creative hypotheses confirms the **₹12.0 Cr campaign** failed "
        "at final-mile operational delivery and checkout fee transparency, rather than customer acquisition."
    )

    # Top KPI Metrics Cards
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    kpi1.metric("Campaign Spend", f"₹{config.TOTAL_CAMPAIGN_SPEND_CR:.1f} Cr", "100% Deployed")
    kpi2.metric("Unrecovered Capital", f"₹{config.UNRECOVERED_CAPITAL_CR:.2f} Cr", "-96.1% Net Loss", delta_color="inverse")
    kpi3.metric("Checkout Abandonment", f"{config.CART_ABANDONMENT_RATE:.1f}%", "3.40 Lakh Drop-Offs", delta_color="inverse")
    kpi4.metric("Blended CAC Overrun", f"₹{config.RECOVERY_TARGETS['Blended CAC (₹)']['actual']:.0f}", "+81% vs ₹420 SLA", delta_color="inverse")
    kpi5.metric("Dark Store OOS", f"{config.OOS_RATE_ACTUAL:.1f}%", "+900 bps vs 2% SLA", delta_color="inverse")

    st.markdown("---")

    col_left, col_right = st.columns([6, 5])

    with col_left:
        st.subheader("Funnel Attrition Waterfall (Lakhs)")
        # Conversion funnel drop-off analysis
        fig_funnel = go.Figure(
            go.Waterfall(
                name="Users",
                orientation="v",
                measure=["relative", "relative", "relative", "total"],
                x=["Site Visits", "App Installs", "Drop-Off at Checkout", "Completed Orders"],
                textposition="outside",
                text=["37.0L", "6.3L", "-3.4L", "2.2L"],
                y=[37.0, -(37.0 - 6.3), -(5.60 - 2.20), 2.20],
                connector={"line": {"color": "#636EFA"}},
                decreasing={"marker": {"color": "#EF553B"}},
                increasing={"marker": {"color": "#00CC96"}},
                totals={"marker": {"color": "#2CA02C"}},
            )
        )
        fig_funnel.update_layout(height=380, margin=dict(t=30, b=20, l=20, r=20))
        st.plotly_chart(fig_funnel, use_container_width=True)

    with col_right:
        st.subheader("Cohort Retention Decay (3-Month Trend)")
        retention_df = pd.DataFrame(
            {
                "Timeline": ["Month 1 (Baseline)", "Month 2 (-1100 bps)", "Month 3 (-800 bps)"],
                "Retention (%)": [config.COHORT_RETENTION_M1, config.COHORT_RETENTION_M2, config.COHORT_RETENTION_M3],
                "Target Recovery (%)": [45.0, 38.0, 30.0],
            }
        )
        fig_decay = px.line(
            retention_df,
            x="Timeline",
            y=["Retention (%)", "Target Recovery (%)"],
            markers=True,
            title="Actual vs Target Cohort Retention Decay",
            color_discrete_sequence=["#EF553B", "#00CC96"],
        )
        fig_decay.update_layout(height=380, yaxis_range=[0, 50], margin=dict(t=30, b=20, l=20, r=20))
        st.plotly_chart(fig_decay, use_container_width=True)

    # Invalidation of False Leads Matrix
    st.subheader("Invalidation of Competing Hypotheses")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info("🎨 **Hypothesis 1: Creative Deficit**")
        st.markdown(
            "- **Ad Recall:** 63% (vs 45% target)\n"
            "- **Video Completion:** 57% (vs 38% target)\n"
            "- **Social Engagement:** 6.4% (vs 3.5% target)\n"
            "**Verdict: Refuted.** High intent generated; collapse occurred post-click."
        )
    with c2:
        st.warning("👥 **Hypothesis 2: Wrong Audience**")
        st.markdown(
            "- **Tier-1 Retention:** 24% | CAC: ₹720\n"
            "- **Tier-2 Retention:** 36% | CAC: ₹510\n"
            "- **Tier-3 Retention:** 42% | CAC: ₹420\n"
            "**Verdict: Refuted.** Urban users switched due to hidden fees and delays."
        )
    with c3:
        st.error("⚙️ **Empirical Root Cause: Operational Breach**")
        st.markdown(
            "- **Checkout Fee Shock:** ₹30–₹50 unannounced charge\n"
            "- **Out-of-Stock (OOS):** 11.0% (vs 2.0% SLA)\n"
            "- **Delivery Delay:** 18.0 min (vs 15.0 min SLA)\n"
            "**Verdict: Verified.** Operational failure broke customer trust."
        )
