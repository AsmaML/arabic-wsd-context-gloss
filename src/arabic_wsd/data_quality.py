"""Validation and summary helpers for context-gloss pair datasets."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass

import pandas as pd


REQUIRED_COLUMNS = ("verb_context", "sense", "label")


@dataclass(frozen=True)
class DatasetSummary:
    """Compact description of a binary context-gloss dataset."""

    instances: int
    positive_labels: int
    negative_labels: int
    unique_contexts: int
    unique_senses: int
    duplicate_rows: int
    conflicting_pairs: int

    def to_dict(self) -> dict[str, int]:
        return asdict(self)


def normalize_text(value: object) -> str:
    """Normalize spacing while preserving Arabic letters and diacritics."""

    text = str(value).strip()
    text = re.sub(r"\s+", " ", text)
    return re.sub(r"\s*,\s*", ",", text)


def _standardize_columns(data: pd.DataFrame) -> pd.DataFrame:
    aliases = {
        "verb+context": "verb_context",
        "verb context": "verb_context",
    }
    frame = data.rename(columns=aliases).copy()

    unnamed = [column for column in frame.columns if str(column).startswith("Unnamed:")]
    if unnamed:
        frame = frame.drop(columns=unnamed)

    missing = [column for column in REQUIRED_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    return frame.loc[:, REQUIRED_COLUMNS]


def prepare_pairs(data: pd.DataFrame) -> pd.DataFrame:
    """Return a normalized copy with a validated binary label column."""

    frame = _standardize_columns(data)

    if frame.isna().any().any():
        null_columns = frame.columns[frame.isna().any()].tolist()
        raise ValueError(f"Null values found in: {', '.join(null_columns)}")

    for column in ("verb_context", "sense"):
        frame[column] = frame[column].map(normalize_text)

    frame["label"] = pd.to_numeric(frame["label"], errors="raise").astype("int8")
    labels = set(frame["label"].unique())
    if not labels.issubset({0, 1}):
        raise ValueError(f"Labels must be binary; found: {sorted(labels)}")

    return frame


def summarize_dataset(data: pd.DataFrame) -> DatasetSummary:
    """Compute label, diversity, duplication and contradiction statistics."""

    frame = prepare_pairs(data)
    label_counts = frame["label"].value_counts()
    labels_per_pair = frame.groupby(["verb_context", "sense"])["label"].nunique()

    return DatasetSummary(
        instances=len(frame),
        positive_labels=int(label_counts.get(1, 0)),
        negative_labels=int(label_counts.get(0, 0)),
        unique_contexts=int(frame["verb_context"].nunique()),
        unique_senses=int(frame["sense"].nunique()),
        duplicate_rows=int(frame.duplicated().sum()),
        conflicting_pairs=int((labels_per_pair > 1).sum()),
    )

