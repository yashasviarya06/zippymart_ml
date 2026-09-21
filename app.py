"""
Zippy Mart Forensic Recovery Engine | Master Application Entry Point.
Controls navigation, caching, hyperparameter sidebars, and modular routing.
"""

import streamlit as st
import config
from data_engine import generate_forensic_checkout_dataset, prepare_features
from ml_models import train_and_evaluate_all_models
from modules import audit_overview, model_comparison, portfolio_realloc, what_if_simulator

# Streamlit Page Setup
st.set_page_config(
    page_title="Zippy Mart | Quick-Commerce ML Diagnostic",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling
# Custom Styling
st.markdown(
    """
    <style>
    .metric-card { background-color: #1E222A; border-radius: 8px; padding: 15px; }
    div[data-testid="stMetricValue"] { font-size: 1.8rem; font-weight: 700; }
    </style>
    """,
    unsafe_allow_html=True,
)


def main():
    st.sidebar.title("🛒 Forensic ML Engine")
    st.sidebar.caption("GLIM Autopsy & Governance Platform")

    # Navigation Menu
    menu_choice = st.sidebar.radio(
        "Navigate Dashboard Modules:",
        [
            "1. Executive Forensic Autopsy",
            "2. ML Model Leaderboard & Matrices",
            "3. What-If Strategy Simulator",
            "4. Capital Realignment & Governance",
        ],
    )

    st.sidebar.markdown("---")
    st.sidebar.subheader("Ensemble Model Hyperparameters")
    rf_trees = st.sidebar.slider("Number of Estimators", 50, 300, 150, step=25)
    rf_depth = st.sidebar.slider("Max Tree Depth", 3, 16, 8)
    xgb_lr = st.sidebar.slider("XGBoost Learning Rate", 0.01, 0.30, 0.05, step=0.01)
    test_split = st.sidebar.slider("Holdout Test Size (%)", 10, 40, 20)

    # 1. Ingest Data Pipeline
    df_raw = generate_forensic_checkout_dataset()
    X, y = prepare_features(df_raw)

    # 2. Train Pipelines
    metrics_df, fitted_models, preds_dict, probs_dict, roc_data, test_context = train_and_evaluate_all_models(
        X, y, test_size=test_split / 100.0, rf_trees=rf_trees, rf_depth=rf_depth, xgb_lr=xgb_lr
    )

    # 3. Route to Modular View
    if menu_choice == "1. Executive Forensic Autopsy":
        audit_overview.render()
    elif menu_choice == "2. ML Model Leaderboard & Matrices":
        model_comparison.render(metrics_df, fitted_models, preds_dict, probs_dict, roc_data, test_context)
    elif menu_choice == "3. What-If Strategy Simulator":
        what_if_simulator.render(fitted_models, test_context)
    elif menu_choice == "4. Capital Realignment & Governance":
        portfolio_realloc.render()


if __name__ == "__main__":
    main()