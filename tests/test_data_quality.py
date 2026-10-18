import unittest

import pandas as pd

from arabic_wsd.data_quality import normalize_text, prepare_pairs, summarize_dataset


def sample_pairs() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "verb+context": [
                "كتب , كتب الطالب الدرس",
                "كتب,كتب الطالب الدرس",
                "كتب,كتب الكاتب رواية",
                "قرأ,قرأ الطفل القصة",
            ],
            "sense": ["خط بالقلم", "ألّف", "ألّف", "طالع النص"],
            "label": [1, 0, 1, 1],
        }
    )


class DataQualityTests(unittest.TestCase):
    def test_normalize_text_preserves_arabic_content(self) -> None:
        self.assertEqual(
            normalize_text("  كتب   ,  كتب الطالب  "),
            "كتب,كتب الطالب",
        )

    def test_prepare_pairs_accepts_original_column_name(self) -> None:
        prepared = prepare_pairs(sample_pairs())
        self.assertEqual(
            list(prepared.columns),
            ["verb_context", "sense", "label"],
        )
        self.assertEqual(prepared.loc[0, "verb_context"], "كتب,كتب الطالب الدرس")

    def test_summary_detects_conflicting_context_gloss_pair(self) -> None:
        data = sample_pairs()
        data.loc[1, "sense"] = "خط بالقلم"

        summary = summarize_dataset(data)

        self.assertEqual(summary.instances, 4)
        self.assertEqual(summary.positive_labels, 3)
        self.assertEqual(summary.negative_labels, 1)
        self.assertEqual(summary.unique_contexts, 3)
        self.assertEqual(summary.conflicting_pairs, 1)

    def test_rejects_non_binary_labels(self) -> None:
        data = sample_pairs()
        data.loc[0, "label"] = 2

        with self.assertRaisesRegex(ValueError, "Labels must be binary"):
            prepare_pairs(data)

    def test_rejects_null_values(self) -> None:
        data = sample_pairs()
        data.loc[0, "sense"] = None

        with self.assertRaisesRegex(ValueError, "Null values found"):
            prepare_pairs(data)


if __name__ == "__main__":
    unittest.main()

