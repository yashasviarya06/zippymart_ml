"""
Machine Learning Training & Performance Evaluation Pipeline.
Implements Random Forest, XGBoost, Gradient Boosting, and Logistic Regression models.
"""

from typing import Any, Dict, List, Tuple
import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier, GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score, roc_curve
from sklearn.model_selection import train_test_split
import streamlit as st
from xgboost import XGBClassifier


@st.cache_resource(show_spinner=False)
def train_and_evaluate_all_models(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float = 0.20,
    rf_trees: int = 150,
    rf_depth: int = 8,
    xgb_lr: float = 0.05,
) -> Tuple[pd.DataFrame, Dict[str, Any], Dict[str, np.ndarray], Dict[str, np.ndarray], Dict[str, Any], Any]:
    """Fits all classification pipelines and computes forensic comparison metrics."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42, stratify=y
    )

    model_registry = {
        "Random Forest": RandomForestClassifier(
            n_estimators=rf_trees, max_depth=rf_depth, min_samples_split=6, random_state=42, n_jobs=-1
        ),
        "XGBoost": XGBClassifier(
            n_estimators=rf_trees,
            max_depth=rf_depth,
            learning_rate=xgb_lr,
            eval_metric="logloss",
            random_state=42,
            n_jobs=-1,
        ),
        "Gradient Boosting": GradientBoostingClassifier(
            n_estimators=rf_trees, max_depth=rf_depth - 2, learning_rate=xgb_lr, random_state=42
        ),
        "Extra Trees": ExtraTreesClassifier(
            n_estimators=rf_trees, max_depth=rf_depth, random_state=42, n_jobs=-1
        ),
        "Logistic Regression": LogisticRegression(max_iter=1000, C=1.0, random_state=42),
    }

    metrics_list = []
    fitted_models = {}
    preds_dict = {}
    probs_dict = {}
    roc_data = {}

    for name, clf in model_registry.items():
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        y_prob = clf.predict_proba(X_test)[:, 1] if hasattr(clf, "predict_proba") else y_pred

        fitted_models[name] = clf
        preds_dict[name] = y_pred
        probs_dict[name] = y_prob

        # Metric evaluations
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        auc = roc_auc_score(y_test, y_prob)

        fpr, tpr, _ = roc_curve(y_test, y_prob)
        roc_data[name] = {"fpr": fpr, "tpr": tpr, "auc": auc}

        metrics_list.append(
            {
                "Model": name,
                "Accuracy": acc,
                "Precision": prec,
                "Recall": rec,
                "F1-Score": f1,
                "ROC-AUC": auc,
            }
        )

    metrics_df = pd.DataFrame(metrics_list).sort_values(by="ROC-AUC", ascending=False).reset_index(drop=True)
    test_context = {"X_test": X_test, "y_test": y_test}

    return metrics_df, fitted_models, preds_dict, probs_dict, roc_data, test_context