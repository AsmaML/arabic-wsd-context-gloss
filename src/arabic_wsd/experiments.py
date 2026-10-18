"""Reusable helpers for the context--gloss classification experiments.

Heavy machine-learning dependencies are imported inside the functions that use
them.  The data-quality utilities therefore remain usable without installing
PyTorch or Transformers.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class ModelConfig:
    checkpoint: str
    epochs: int


MODEL_CONFIGS: dict[str, ModelConfig] = {
    "arabert": ModelConfig("aubmindlab/bert-base-arabertv02", 4),
    "camelbert": ModelConfig("CAMeL-Lab/bert-base-arabic-camelbert-msa", 4),
    "arbertv2": ModelConfig("UBC-NLP/ARBERTv2", 2),
    "arabic-albert": ModelConfig("asafaya/albert-base-arabic", 4),
}


def load_pairs(path: str | Path) -> pd.DataFrame:
    """Load a context--gloss workbook and validate its public schema."""
    frame = pd.read_excel(path)
    frame = frame.loc[:, ~frame.columns.astype(str).str.startswith("Unnamed:")]
    required = ["verb+context", "sense", "label"]
    missing = [column for column in required if column not in frame.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    frame = frame[required].copy()
    frame["verb+context"] = frame["verb+context"].astype("string").str.strip()
    frame["sense"] = frame["sense"].astype("string").str.strip()
    frame["label"] = pd.to_numeric(frame["label"], errors="raise").astype("int64")

    if frame[["verb+context", "sense", "label"]].isna().any().any():
        raise ValueError("The dataset contains missing values in required columns")
    if not set(frame["label"].unique()).issubset({0, 1}):
        raise ValueError("Labels must be binary: 0 or 1")
    return frame


def classification_metrics(labels: np.ndarray, predictions: np.ndarray) -> dict[str, float]:
    """Compute the four binary-classification metrics reported in paper 2."""
    labels = np.asarray(labels)
    predictions = np.asarray(predictions)
    true_positive = int(((labels == 1) & (predictions == 1)).sum())
    false_positive = int(((labels == 0) & (predictions == 1)).sum())
    false_negative = int(((labels == 1) & (predictions == 0)).sum())
    precision = true_positive / (true_positive + false_positive) if true_positive + false_positive else 0.0
    recall = true_positive / (true_positive + false_negative) if true_positive + false_negative else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "accuracy": float((labels == predictions).mean()),
        "f1": float(f1),
        "precision": float(precision),
        "recall": float(recall),
    }


def fit_logistic_stack(
    validation_features: np.ndarray,
    validation_labels: np.ndarray,
    test_features: np.ndarray,
    test_labels: np.ndarray,
    *,
    seed: int = 9,
) -> tuple[object, dict[str, float]]:
    """Fit a logistic-regression stacker and evaluate it on the held-out test set."""
    from sklearn.linear_model import LogisticRegression

    meta_model = LogisticRegression(random_state=seed, max_iter=1_000)
    meta_model.fit(validation_features, validation_labels)
    predictions = meta_model.predict(test_features)
    return meta_model, classification_metrics(test_labels, predictions)
