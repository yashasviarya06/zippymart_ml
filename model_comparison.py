"""
Model Comparison & Confusion Matrix Engine.
Renders side-by-side metric benchmarks, interactive confusion matrices, and ROC curves.
"""

from typing import Any, Dict
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import confusion_matrix
import streamlit as st


def render(
    metrics_df: pd.DataFrame,
    fitted_models: Dict[str, Any],
    preds_dict: Dict[str, Any],
    probs_dict: Dict[str, Any],
    roc_data: Dict[str, Any],
    test_context: Dict[str, Any],
):
    st.header("2. ML Model Performance & Error Matrix Diagnostic")
    st.markdown(
        "Benchmarking classification architectures to identify probability of cart abandonment. "
        "Tree ensemble models (Random Forest, XGBoost) capture complex non-linear SLA interaction thresholds."
    )

    # 1. Metric Leaderboard Table
    st.subheader("Model Evaluation Leaderboard")
    st.dataframe(
        metrics_df.style.format(
            {
                "Accuracy": "{:.4f}",
                "Precision": "{:.4f}",
                "Recall": "{:.4f}",
                "F1-Score": "{:.4f}",
                "ROC-AUC": "{:.4f}",
            }
        ).highlight_max(axis=0, color="#1B4D3E"),
        use_container_width=True,
    )

    # 2. Metric Comparison Bar Chart
    melted_metrics = metrics_df.melt(
        id_vars=["Model"], var_name="Metric", value_name="Score"
    )
    fig_bars = px.bar(
        melted_metrics,
        x="Metric",
        y="Score",
        color="Model",
        barmode="group",
        title="Multi-Model Performance Across Core Classification Metrics",
    )
    fig_bars.update_layout(yaxis_range=[0.5, 1.0], height=380)
    st.plotly_chart(fig_bars, use_container_width=True)

    st.markdown("---")

    # 3. Interactive Confusion Matrix Deep-Dive
    st.subheader("Interactive Confusion Matrix Diagnostic")
    selected_model_cm = st.selectbox(
        "Select Model for Confusion Matrix Inspection:",
        list(fitted_models.keys()),
        index=1,
    )

    y_test = test_context["y_test"]
    y_pred = preds_dict[selected_model_cm]
    cm = confusion_matrix(y_test, y_pred)

    col_cm, col_roc = st.columns([5, 6])

    with col_cm:
        annotated_text = [
            [
                f"TN: {cm[0][0]}<br>({cm[0][0]/len(y_test):.1%})",
                f"FP: {cm[0][1]}<br>({cm[0][1]/len(y_test):.1%})",
            ],
            [
                f"FN: {cm[1][0]}<br>({cm[1][0]/len(y_test):.1%})",
                f"TP: {cm[1][1]}<br>({cm[1][1]/len(y_test):.1%})",
            ],
        ]
        x_cats = ["Predicted Abandoned (0)", "Predicted Converted (1)"]
        y_cats = ["Actual Abandoned (0)", "Actual Converted (1)"]

        # Native go.Heatmap replaces ff.create_annotated_heatmap
        fig_cm = go.Figure(
            data=go.Heatmap(
                z=cm,
                x=x_cats,
                y=y_cats,
                text=annotated_text,
                texttemplate="%{text}",
                textfont={"size": 13},
                colorscale="Blues",
                showscale=True,
            )
        )
        fig_cm.update_yaxes(autorange="reversed")
        fig_cm.update_layout(
            title=f"{selected_model_cm} Confusion Matrix",
            height=380,
            margin=dict(t=40, b=20, l=20, r=20),
        )
        st.plotly_chart(fig_cm, use_container_width=True)

    with col_roc:
        # ROC-AUC Multi-Curve Overlay
        fig_roc = go.Figure()
        for name, rdata in roc_data.items():
            fig_roc.add_trace(
                go.Scatter(
                    x=rdata["fpr"],
                    y=rdata["tpr"],
                    mode="lines",
                    name=f"{name} (AUC = {rdata['auc']:.3f})",
                )
            )
        fig_roc.add_trace(
            go.Scatter(
                x=[0, 1],
                y=[0, 1],
                mode="lines",
                line=dict(dash="dash", color="grey"),
                name="Baseline (0.50)",
            )
        )
        fig_roc.update_layout(
            title="Receiver Operating Characteristic (ROC) Comparison",
            xaxis_title="False Positive Rate",
            yaxis_title="True Positive Rate",
            height=380,
            margin=dict(t=40, b=20, l=20, r=20),
        )
        st.plotly_chart(fig_roc, use_container_width=True)

    # 4. Feature Importance Extraction
    st.subheader("Algorithmic Root Cause: Feature Importance Ranking")
    if hasattr(fitted_models[selected_model_cm], "feature_importances_"):
        X_test = test_context["X_test"]
        importances = fitted_models[selected_model_cm].feature_importances_
        feat_df = pd.DataFrame(
            {"Feature": X_test.columns, "Importance": importances}
        ).sort_values(by="Importance", ascending=True)

        fig_imp = px.bar(
            feat_df,
            x="Importance",
            y="Feature",
            orientation="h",
            color="Importance",
            color_continuous_scale="Viridis",
            title=f"Feature Importances from {selected_model_cm}",
        )
        fig_imp.update_layout(height=350)
        st.plotly_chart(fig_imp, use_container_width=True)
    else:
        st.info(
            "Linear models evaluate linear coefficients rather than Gini/tree-based feature importances."
        )