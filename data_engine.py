"""
Data Simulation & Preprocessing Engine.
Synthesizes user-level checkout records matching empirical distributions.
"""

import numpy as np
import pandas as pd
import streamlit as st


@st.cache_data(show_spinner=False)
def generate_forensic_checkout_dataset(n_samples: int = 12000, seed: int = 42) -> pd.DataFrame:
    """Generates synthetic dataset calibrated to ~39.29% conversion and 60.71% drop-off."""
    np.random.seed(seed)

    # 1. Acquisition Channels with historical distribution weights
    channels = [
        "Google Search",
        "Dynamic Retargeting",
        "Instagram Reels",
        "Micro-Influencers",
        "YouTube Consideration",
        "Affiliate Networks",
    ]
    ch_weights = [0.29, 0.22, 0.18, 0.11, 0.14, 0.06]
    channel = np.random.choice(channels, size=n_samples, p=ch_weights)

    # 2. Geographic Tier Distribution
    tiers = ["Tier-1", "Tier-2", "Tier-3"]
    tier_weights = [0.55, 0.25, 0.20]
    tier = np.random.choice(tiers, size=n_samples, p=tier_weights)

    # 3. Operational features: 18 min delivery SLA overrun, 11% OOS, 83% partner fill rate
    delivery_time = np.clip(np.random.normal(loc=18.0, scale=3.6, size=n_samples), 10.0, 36.0)
    oos_rate = np.clip(np.random.normal(loc=11.0, scale=3.2, size=n_samples), 1.0, 25.0)
    partner_avail = np.clip(np.random.normal(loc=83.0, scale=5.2, size=n_samples), 55.0, 99.0)

    # 4. Cart Value centered on ₹520 AOV
    cart_value = np.clip(np.random.normal(loc=520.0, scale=125.0, size=n_samples), 140.0, 1600.0)

    # 5. Unannounced Fee Shock (₹30-₹50) on 65% of carts lacking upfront transparency
    fee_shock_mask = np.random.rand(n_samples) > 0.35
    fee_shock = np.where(fee_shock_mask, np.random.uniform(30.0, 50.0, size=n_samples), 0.0)

    # 6. Latent Logistic Probability Model
    log_odds = (
        0.82
        - (fee_shock * 0.076)  # Primary drop-off driver
        - ((delivery_time - 15.0) * 0.142)  # Delivery SLA slippage penalty
        - ((oos_rate - 2.0) * 0.088)  # Stockout penalty
        + ((partner_avail - 83.0) * 0.028)  # Partner availability gain
        + (cart_value * 0.00075)  # Basket resilience
    )

    channel_modifiers = {
        "Google Search": 0.44,
        "Dynamic Retargeting": 0.52,
        "Instagram Reels": -0.38,
        "Micro-Influencers": -0.48,
        "YouTube Consideration": -0.28,
        "Affiliate Networks": -0.24,
    }
    for ch, mod in channel_modifiers.items():
        log_odds[channel == ch] += mod

    tier_modifiers = {"Tier-1": -0.22, "Tier-2": 0.24, "Tier-3": 0.34}
    for t, mod in tier_modifiers.items():
        log_odds[tier == t] += mod

    probabilities = 1.0 / (1.0 + np.exp(-log_odds))
    converted = (probabilities >= 0.50).astype(int)

    df = pd.DataFrame(
        {
            "acquisition_channel": channel,
            "city_tier": tier,
            "cart_value": np.round(cart_value, 2),
            "fee_shock": np.round(fee_shock, 2),
            "delivery_time_min": np.round(delivery_time, 1),
            "hub_oos_rate": np.round(oos_rate, 2),
            "partner_availability_pct": np.round(partner_avail, 2),
            "conversion_prob": np.round(probabilities, 4),
            "checkout_completed": converted,
        }
    )
    return df


def prepare_features(df: pd.DataFrame):
    """One-hot encodes categorical dimensions for machine learning pipelines."""
    df_encoded = pd.get_dummies(
        df.drop(columns=["conversion_prob"]),
        columns=["acquisition_channel", "city_tier"],
        drop_first=True,
    )
    X = df_encoded.drop(columns=["checkout_completed"])
    y = df_encoded["checkout_completed"]
    return X, y