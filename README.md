# icr-classical-nlp

## Summary:

Lemmatization is a vital first step in Latin natural language processing, which enables further computational analysis of Latin texts. In this project, I tested and compared the capabilities and algorithmic strategies of various Latin lemmatizers and their components. In particular, I examined the Backoff strategy of lemmatization and compared it with the promising but unexpectedly unused Ensemble method.

## Instructions for Use:

Install the CLTK library with
```
pip install cltk
```
Then use 
```
git clone git@github.com:jmohta1/icr-classical-nlp.git
```
For examples of the individual CLTK lemmatizers, run ```lemmatizer_example()``` in lemma_tester.py.
For examples of data generation, run data_collection.py.

## Introduction:

In natural language processing, an important first step is to reduce tokens (grammatical chunks, e.g. words or punctuation) into simpler forms. For many languages, including English, the most efficient method is stemming, removing prefixes and suffixes to get a word's base form [CITE]. However, in some classical languages, including Latin, simple stemming algorithms are no longer effective, largely due to the many forms of each word and similar forms between different kinds of words. Instead, better results can be obtained by creating algorithms to analyze each word and figure out its base form, called its lemma [CITE]. These algorithms, called lemmatizers, employ a wide variety of different methods to lemmatize words. In this project, I focused on Latin lemmatizers' efficacy in analyzing tokens from Caesar's De Bello Gallico. I primarily experimented with the Classical Language Toolkit's Backoff Lemmatizer pipeline. 


## Background:

In a Backoff lemmatizer, multiple sub-lemmatizers are employed in a chain. Given a token, the pipeline's first sub-lemmatizer attempts to find a lemma match. If it can, the system moves on to the next token. Otherwise, the next sub-lemmatizer attempts to find a lemma. The process continues until every token has a lemma. 

The Backoff system's optimal sub-lemmatizer chain involves having high-accuracy, low-yield lemmatizers first, then moving on to more well-rounded lemmatizers, and finally placing high-yield lemmatizers, no matter their accuracy. This way, if the most accurate lemmatizers (typically those based on a dictionary) have a match, it gets implemented. If not, the next lemmatizers, more fallible but wider in yield, can search for a lemma that will likely be correct. More often than the others, these lemmatizers are based on some kind of training algorithm [CITE]. Finally, a catch-all sub-lemmatizer will run, ensuring that every word has at least some lemma.

CLTK's Latin Backoff Lemmatizer employs a strategy fairly similar to the above. First, the DictLemmatizer consults a dictionary of word forms to find a lemma match. It only registers a match if it happens to find a perfect pair, so it leaves many words blank. Then, the UnigramLemmatizer, based on training data of lemmatized tokens, looks for lemmas. Next, the CLTK Backoff chain includes lemmatizers that are inaccurate but better than the catch-all algorithms, on the slight chance that one of these lemmatizers will match tokens correctly. The first of the two lemmatizers in this category is the Regexp Lemmatizer, which consults a list of typical shifts to make (e.g. removing the -ere infinitive verb ending for an -o first person singular ending). This method, similar to English stemming, is not very accurate in Latin but is sometimes correct. Next comes another version of the DictLemmatizer, which consults a larger but less accurate dictionary. Last are the catch-all sub-lemmatizers: IdentityLemmatizer simply returns its input, which will be correct if the token happens to be in its base form. Finally, the DefaultLemmatizer returns a default output no matter its input, ensuring that every token gets some lemma even if all the others fail.

This project tests each CLTK sub-lemmatizer individually, and it experiments with adding the Simplemma lemmatizer to the Backoff chain. It also explores the CLTK legacy code for the Ensemble lemmatization system. Using Julius Caesar's De Bello Gallico Book 1, Chapter 1, I collected and analyzed data on the lemmatizers' accuracy.
