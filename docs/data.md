# Data documentation

## Purpose

The data was created for supervised Arabic verb sense disambiguation. Each instance associates:

- a target Arabic verb and one of its usage contexts;
- a candidate sense definition, or gloss;
- a binary label indicating whether the gloss matches the meaning expressed in that context.

The linguistic material was derived from the Arramooz Alwaseet dictionary through three stages: source preparation, construction of a verb sense inventory and generation of labeled context–gloss pairs.

## Construction

The construction process began with Arabic verbs, usage examples and definitions extracted from Arramooz Alwaseet. The records were cleaned and normalized before the sense inventory and labeled pairs were produced.

### Verb sense inventory

The intermediate sense inventory contains 35,980 records and 9,441 distinct verb strings. The task was then restricted to ambiguous verbs before generating labeled context–gloss pairs.

### Initial labeled dataset

The initial labeled dataset contains 51,856 instances:

- 26,091 positive labels;
- 25,765 negative labels;
- 25,321 distinct `verb+context` strings.

This dataset supports the experiments reported in *Exploring the Impact of Stop Words and Particles on Arabic Word Sense Disambiguation*.

### Revised labeled dataset

The revised labeled dataset contains 51,161 instances:

- 25,721 positive labels;
- 25,440 negative labels;
- 25,239 distinct `verb+context` strings.

This revision supports the individual and ensemble BERT experiments. Contradictory labels for identical normalized context–gloss pairs were removed during the revision.

## Availability

Both labeled dataset versions are publicly available in the [`data`](../data/) directory:

- [initial labeled dataset](../data/arabic_verb_context_gloss_pairs_initial.xlsx);
- [revised labeled dataset](../data/arabic_verb_context_gloss_pairs_revised.xlsx).

The linguistic material was derived from the Arramooz Alwaseet dictionary. Users should cite the publication associated with the dataset version they use.

Both dataset versions retain the **CC BY 4.0** license used for their original Figshare deposits. See the repository's [data license](../DATA_LICENSE.md) for attribution instructions and source-material information.

