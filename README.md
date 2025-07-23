# latin-lemmatization

## Summary:

Lemmatization is a vital first step in Latin natural language processing, which enables further computational analysis of Latin texts. In this project, I tested and compared the capabilities and algorithmic strategies of various Latin lemmatizers and their components. In particular, I examined the Backoff strategy of lemmatization and compared it with the promising but unexpectedly unused Ensemble method.

## Instructions for Use:

This project must be run on Python 3.9; change your Python version or enter a virtual environment.

First clone the repo with
```
git clone git@github.com:jmohta1/icr-classical-nlp.git
```

Then install the CLTK library with
```
pip install cltk
```
For examples of the individual CLTK lemmatizers, run ```lemmatizer_example()``` in lemma_tester.py.
For examples of plot generation, run 
```
python3 data_collection.py
```
from this directory.
 Your result should look something like below.
 

<img width="640" height="480" alt="sub_lemmatizer_comparison" src="https://github.com/user-attachments/assets/bdc6b750-7861-47af-9582-a3a05629f961" />
