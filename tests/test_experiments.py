import unittest

import numpy as np

from arabic_wsd.experiments import classification_metrics


class ExperimentHelpersTests(unittest.TestCase):
    def test_classification_metrics(self):
        labels = np.array([0, 0, 1, 1])
        predictions = np.array([0, 1, 1, 1])
        metrics = classification_metrics(labels, predictions)

        self.assertAlmostEqual(metrics["accuracy"], 0.75)
        self.assertAlmostEqual(metrics["precision"], 2 / 3)
        self.assertAlmostEqual(metrics["recall"], 1.0)
        self.assertAlmostEqual(metrics["f1"], 0.8)


if __name__ == "__main__":
    unittest.main()
