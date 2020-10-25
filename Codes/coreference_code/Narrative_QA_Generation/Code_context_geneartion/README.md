## Infilling by Language Modeling (ILM)

This repository houses the code for the ILM framework outlined in the ACL 2020 paper [_Enabling language models to fill in the blanks_](https://arxiv.org/abs/2005.05339) (Donahue et al. 2020).

This codebase allows you to fine tune GPT-2 to _infill_, i.e., perform text generation conditioned on both past and future context. For example, you could train GPT-2 to infill proper nouns in news articles, or generate lines of poetry in the middle of the stanza.

An interactive webdemo can be found at [chrisdonahue.com/ilm](https://chrisdonahue.com/ilm).

## Installation

We recommend installing this package using `virtualenv`. After activating the virtual environment, run the following commands:
1. `pip install -r requirements.txt`
1. `python -c "import nltk; nltk.download('punkt')"`
1. `pip install -e .`

## Training a new model

The ILM framework involves a two step process of (1) creating ILM training examples by randomly masking training data, and (2) fine-tuning GPT-2 on those examples. This section walks through an example of this process for one of the built-in datasets and mask functions.

### Creating ILM training examples

The process of creating ILM examples involves randomly masking spans in complete text. For example, if the original text is `She ate leftover pasta for lunch`, an ILM example might look like `She ate [blank] for [blank] [sep] leftover pasta [answer] lunch [answer]`. For efficiency reasons, this codebase generates these examples up front before training.

### Custom datasets

To add a new dataset, first split it into three files: `train.txt`, `valid.txt`, `test.txt`. These files each contain complete documents separated by _three_ newline characters, i.e., `'\n\n\n'.join(documents)`. Then, run `create_ilm_examples.py` with the following arguments: `--data_name custom --data_dir path/to/directory/with/splits`.

### Custom mask functions

A mask function takes text and outputs random spans to masked which correspond to intended downstream behavior. By default, this repository trains ILM models which can infill words, ngrams, sentences, paragraphs, and entire documents.

You can add your own mask functions to perform different infilling tasks. A mask function takes as input a complete document and outputs a list of 3-tuples consisting of `(infilling type, span offset, span length)`, where offset and length are measured in characters.

You can add your custom mask function to [`ilm.mask.custom`](https://github.com/chrisdonahue/ilm_final/blob/master/ilm/mask/custom.py), where there are already two simple examples:

- `ilm.mask.custom.MaskPunctuation`: Masks each punctuation token with 50% probability. Special infilling type for sentence terminals.
- `ilm.mask.custom.MaskProperNoun`: Masks all (detected) proper nouns with 100% probability.

Once you add your mask function, you should pass it as an argument to `create_ilm_examples.py` and `train_ilm.py` scripts e.g.: `--mask_cls ilm.mask.custom.YourCustomMaskFn`.

## Infilling with a trained model

See `inference.ipynb` for an example of how to perform infilling with a trained model. If you prefer, you may also run this notebook on [Google Colab](https://colab.research.google.com/drive/1So95M0hHefyNm_eELglCna_ZayoDX6KV?usp=sharing).
