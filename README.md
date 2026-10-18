# Arabic Verb WSD with Context–Gloss Pairs

This repository presents the main experimental work from my doctoral research on Arabic Word Sense Disambiguation (WSD). The research studies Arabic verb senses through context–gloss matching, with particular attention to linguistic markers, stop words, particles and ensemble methods.

Arabic remains a low-resource language for supervised WSD. To support these experiments, I constructed and revised a dataset of labeled context–gloss pairs from examples and definitions in the Arramooz Alwaseet dictionary. I then treated WSD as a binary sequence-pair classification task: given a verb in context and a candidate gloss, the model predicts whether the gloss expresses the intended sense.

The repository documents the dataset design, experimental settings and results reported in the two publications associated with this work.

## Research questions

The work addresses two questions:

1. What happens to Arabic WSD performance when stop words and particles are retained or removed?
2. Can ensembles of Arabic BERT-based models improve context–gloss classification over individual models?

## Main contributions

- Construction of a large labeled resource for Arabic verb senses in a low-resource setting.
- Comparison of five preprocessing configurations involving stop words, particles and segmentation.
- Fine-tuning and comparison of AraBERT, CAMeLBERT, ARBERTv2 and Arabic ALBERT.
- Evaluation of stacked ensembles built from complementary Arabic language models.
- Analysis of dataset quality and revision of ambiguous or contradictory instances.

## Dataset lineage

| Research stage | Instances | Positive | Negative | Use |
|---|---:|---:|---:|---|
| Initial labeled dataset | 51,856 | 26,091 | 25,765 | Stop-word and particle experiments |
| Revised dataset | 51,161 | 25,721 | 25,440 | Individual and ensemble BERT experiments |

An additional quality-control stage produced the revised dataset by removing problematic cases and regularizing the representation of context–gloss pairs. See [the data documentation](docs/data.md) for details.

Both dataset versions are available in the repository:

- [initial labeled dataset](data/arabic_verb_context_gloss_pairs_initial.xlsx);
- [revised labeled dataset](data/arabic_verb_context_gloss_pairs_revised.xlsx).

The datasets retain the [CC BY 4.0 license](DATA_LICENSE.md) used for their original Figshare deposits. The source dictionary and the associated publications are credited in the license notice.

## Published results

### Stop words and particles

Five dataset variants were evaluated with AraBERTv2. The best F1-score was obtained when stop words, including particles, were retained.

| Dataset version | Accuracy | F1-score |
|---|---:|---:|
| Version 1 | 70.86% | **78.95%** |
| Version 2 | 65.17% | 65.73% |
| Version 3 | **74.41%** | 75.65% |
| Version 4 | 69.45% | 71.69% |
| Version 5 | 74.25% | 76.44% |

The definitions of the five variants and their preprocessing choices are documented in [the experiment notes](docs/experiments.md).

### Ensemble BERT-based models

The strongest ensemble combined AraBERT and ARBERTv2.

| Model | Accuracy | F1-score | Precision | Recall |
|---|---:|---:|---:|---:|
| AraBERT | 81.53% | 81.47% | — | — |
| CAMeLBERT | 79.46% | 79.45% | — | — |
| ARBERTv2 | 80.19% | 80.15% | — | — |
| Arabic ALBERT | 75.25% | 75.23% | — | — |
| AraBERT + CAMeLBERT | 81.61% | 82.41% | 79.11% | 85.99% |
| **AraBERT + ARBERTv2** | **82.11%** | **82.97%** | **79.35%** | **86.93%** |
| AraBERT + CAMeLBERT + ARBERTv2 | 81.88% | 82.69% | 79.30% | 86.38% |
| All four models | 81.94% | 82.76% | 79.32% | 86.51% |

Adding more base models did not automatically improve the ensemble. The two-model AraBERT–ARBERTv2 combination produced the best balance in these experiments.

## Code

The `arabic_wsd.data_quality` module provides the first reusable part of the project. It standardizes the context–gloss schema, normalizes spacing, validates binary labels and reports duplicates or contradictory labels.

The notebooks follow the experimental workflow:

1. [Dataset overview](notebooks/01_dataset_overview.ipynb): task definition, annotated examples, dataset lineage and quality indicators.
2. [Data preparation](notebooks/02_data_preparation.ipynb): schema validation, label checks and the 80/10/10 split used for the ensemble experiments.
3. [Base-model training](notebooks/03_train_base_models.ipynb): paired-sequence tokenization and fine-tuning of AraBERT, CAMeLBERT, ARBERTv2 and Arabic ALBERT.
4. [Ensemble stacking](notebooks/04_ensemble_stacking.ipynb): generation of stacking features, logistic-regression ensembles and comparison of model combinations.

```python
import pandas as pd

from arabic_wsd.data_quality import summarize_dataset

pairs = pd.read_excel("data/arabic_verb_context_gloss_pairs_revised.xlsx")
summary = summarize_dataset(pairs)
print(summary.to_dict())
```

Install the project and run the tests with:

```bash
python -m pip install -e .
python -m unittest discover -s tests
```

Install the optional training dependencies with:

```bash
python -m pip install -e ".[experiments]"
```

Training the four transformer models is intended for a CUDA-capable environment. Generated checkpoints and prediction artifacts are excluded from version control.

## Publications

1. Asma Djaidri, Hassina Aliane and Hamid Azzoune. “Exploring the Impact of Stop Words and Particles on Arabic Word Sense Disambiguation.” *Arabic Language Processing: From Theory to Practice*, ICALP 2024, CCIS 2340, pp. 30–40. [DOI: 10.1007/978-3-031-80438-0_3](https://doi.org/10.1007/978-3-031-80438-0_3).
2. Asma Djaidri, Hassina Aliane and Hamid Azzoune. “Enhancing Arabic Word Sense Disambiguation with Ensemble BERT-Based Models.” *Arabic Language Processing: From Theory to Practice*, ICALP 2024, CCIS 2339, pp. 261–272. [DOI: 10.1007/978-3-031-79164-2_23](https://doi.org/10.1007/978-3-031-79164-2_23).

## Author

Asma Djaidri  
PhD in Artificial Intelligence — Natural Language Processing and Arabic language technologies

