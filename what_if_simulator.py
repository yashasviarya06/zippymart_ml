"""
What-If Strategy Simulator & Operational Kill Switch Engine.
Provides real-time interactive parameter adjustment and policy alert generation.
"""

from typing import Any, Dict
import numpy as np
import pandas as pd
import streamlit as st
import config


def render(fitted_models: Dict[str, Any], test_context: Dict[str, Any]):
    st.header("3. What-If Strategy Simulator & SLA Circuit Breakers")
    st.markdown(
        "Simulate adjustments to pricing transparency, dark-store fulfillment speed, and inventory depth "
        "to forecast customer checkout probability against the non-negotiable governance milestones."
    )

    eval_model = fitted_models.get("XGBoost", fitted_models.get("Random Forest"))
    X_cols = test_context["X_test"].columns

    st.subheader("Interactive Checkout Scenario Parameters")
    col1, col2, col3 = st.columns(3)

    with col1:
        sim_fee = st.slider(
            "Checkout Surprise Fee Shock (₹)",
            0,
            50,
            0,
            step=5,
            help="Hidden fees at payment gateway",
        )
        sim_cart = st.number_input(
            "Cart Basket Value (₹)", min_value=150, max_value=2000, value=560, step=50
        )

    with col2:
        sim_time = st.slider(
            "Estimated Delivery SLA (Mins)",
            10.0,
            30.0,
            15.0,
            step=0.5,
            help="15 min brand promise",
        )
        sim_oos = st.slider(
            "Local Dark-Store OOS Rate (%)",
            1.0,
            20.0,
            3.5,
            step=0.5,
            help="Target recovery SLA: <= 3.5%",
        )

    with col3:
        sim_channel = st.selectbox(
            "Acquisition Channel",
            [
                "Google Search",
                "Dynamic Retargeting",
                "Instagram Reels",
                "Micro-Influencers",
                "YouTube Consideration",
                "Affiliate Networks",
            ],
            index=0,
        )
        sim_tier = st.selectbox("City Tier", ["Tier-1", "Tier-2", "Tier-3"], index=1)

    # Build evaluation vector
    record = {
        "cart_value": float(sim_cart),
        "fee_shock": float(sim_fee),
        "delivery_time_min": float(sim_time),
        "hub_oos_rate": float(sim_oos),
        "partner_availability_pct": 94.0,  # Benchmark recovery SLA
    }
    for col in X_cols:
        if col.startswith("acquisition_channel_"):
            record[col] = 1 if sim_channel == col.replace("acquisition_channel_", "") else 0
        elif col.startswith("city_tier_"):
            record[col] = 1 if sim_tier == col.replace("city_tier_", "") else 0

    df_sample = pd.DataFrame([record])[X_cols]
    prob_conversion = float(eval_model.predict_proba(df_sample)[0][1] * 100.0)

    st.markdown("---")
    st.subheader("Forensic Prediction & Policy Triggers")

    res_col1, res_col2 = st.columns([5, 7])

    with res_col1:
        st.metric(
            label="Predicted Checkout-to-Payment Probability",
            value=f"{prob_conversion:.1f}%",
            delta=f"{prob_conversion - config.RECOVERY_TARGETS['Checkout Conversion (%)']['actual']:.1f}% vs Historical Actual (39.3%)",
        )
        progress_val = float(min(max(prob_conversion / 100.0, 0.0), 1.0))
        st.progress(progress_val)

    with res_col2:
        # Governance Circuit Breakers (Kill Switches)
        st.markdown("**Non-Negotiable SLA Governance Compliance:**")
        if sim_fee > 0:
            st.error(
                f"🛑 **KILL TRIGGER 1: UNANNOUNCED FEE (₹{sim_fee})**\n"
                "Violates radical transparency mandate. Induces 60.7% cart drop-off."
            )
        else:
            st.success("✅ **Transparent Pricing Verified:** Zero hidden checkout markup.")

        if sim_oos > 6.0:
            st.warning(
                "⚠️ **KILL TRIGGER 3A: OOS BREAKER ACTIVE**\n"
                "Dark-store OOS exceeds 6.0% circuit-breaker threshold. Ad spend in this hub must pause within 48 hrs."
            )
        elif sim_oos <= 3.5:
            st.success("✅ **Inventory SLA Compliant:** OOS at or below 60-day recovery benchmark (3.5%).")

        if sim_time > 17.0:
            st.error(
                "🛑 **KILL TRIGGER 3B: SLA SLIPPAGE BREAKER**\n"
                "Delivery exceeds 17 mins. Paid acquisition must freeze until rider capacity normalizes."
            )
        elif sim_time <= 15.0:
            st.success("✅ **Delivery SLA Restored:** Meeting the 15-minute speed promise.")

        if prob_conversion >= 62.0:
            st.success("🎯 **60-Day Milestone Achieved:** Conversion meets or exceeds the 62.0% turnaround target.")
        else:
            st.info(
                "ℹ️ **Optimization Needed:** Bring delivery under 15 mins and OOS below 3.5% to achieve the 62% recovery milestone."
            )