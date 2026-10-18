# Arabic verb context–gloss datasets

This directory contains the two dataset versions used in the published Arabic Word Sense Disambiguation experiments.

## Files

- [`arabic_verb_context_gloss_pairs_initial.xlsx`](arabic_verb_context_gloss_pairs_initial.xlsx): 51,856 labeled pairs used for the stop-word and particle experiments.
- [`arabic_verb_context_gloss_pairs_revised.xlsx`](arabic_verb_context_gloss_pairs_revised.xlsx): 51,161 labeled pairs used for the individual and ensemble BERT experiments.

## Columns

| Column | Description |
|---|---|
| `verb+context` | Arabic target verb followed by a usage context |
| `sense` | Candidate dictionary gloss for the target verb |
| `label` | `1` when the gloss matches the contextual meaning, otherwise `0` |

The first unnamed column stores the original row index and is not a model feature.

## Citation

If you use these datasets, cite the publication associated with the relevant version. Full references and DOI links are available in the [repository README](../README.md#publications).

The datasets are distributed under [CC BY 4.0](../DATA_LICENSE.md), consistently with their original Figshare deposits:

- [initial dataset on Figshare](https://figshare.com/s/55791aea9cc5f7509f01);
- [revised dataset on Figshare](https://figshare.com/s/9c558f732bf5afb08217).

The linguistic material was derived from the Arramooz Alwaseet dictionary and remains subject to the source project's attribution and license requirements. See the [data documentation](../docs/data.md) for the construction process and experimental use.

