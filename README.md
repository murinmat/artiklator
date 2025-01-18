# Artiklator
A simple python package for German article determination and other utils.

## Usage

The most basic use-case of the usage of this package is determination of the article for a given german noun with an optional translation added.

```python
>>> from artiklator import articlerize

>>> result = articlerize('Hund')
>>> print(result.article, result.german_noun)
der Hund
>>> result = articlerize('Hund', 'en')
>>> print(result.article, result.german_noun, ',', result.translation)
der Hund , Dog
```
