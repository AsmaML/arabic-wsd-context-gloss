# Experiment notes

## Paper 1: stop words and particles

The first study used AraBERTv2 for binary classification of Arabic verb context–gloss pairs. Five versions of the dataset were constructed to compare segmentation and the treatment of stop words and particles.

| Version | Preprocessing condition | Accuracy | F1-score |
|---|---|---:|---:|
| 1 | Segmentation; stop words and particles retained | 70.86% | 78.95% |
| 2 | Segmentation; all stop words removed | 65.17% | 65.73% |
| 3 | Segmentation; particles removed | 74.41% | 75.65% |
| 4 | No segmentation; stop words removed | 69.45% | 71.69% |
| 5 | No segmentation; stop words retained | 74.25% | 76.44% |

The main observation is not that one preprocessing choice dominates every metric. Version 3 obtained the highest accuracy, while Version 1 obtained the highest F1-score. Removing all stop words produced the weakest result among the segmented variants.

## Paper 2: ensemble BERT models

Four Arabic pretrained language models were fine-tuned on the revised dataset:

- AraBERT;
- CAMeLBERT-MSA;
- ARBERTv2;
- Arabic ALBERT.

Their outputs were combined through a stacking strategy with a logistic-regression meta-model. Pairwise, three-model and four-model combinations were compared.

The best configuration combined AraBERT and ARBERTv2:

- accuracy: 82.11%;
- F1-score: 82.97%;
- precision: 79.35%;
- recall: 86.93%.

The four-model ensemble reached 81.94% accuracy and 82.76% F1-score. This result is useful because it shows that ensemble size alone was not the determining factor; the complementarity of the selected models mattered more.


