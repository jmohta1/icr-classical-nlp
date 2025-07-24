from cltk.lemmatize.backoff import *
from cltk.lemmatize.lat import LatinBackoffLemmatizer
from cltk.utils.file_operations import open_pickle
from cltk.lemmatize.lat import latin_sub_patterns
from utils.custom_pipeline import Backoff, Ensemble
from ensemble import *
import simplemma

"""Houses all the lemmatizers used in testing."""

#-------------training/reference data----------------

#example regular expressions for regex lemmatizer
reg = [("as", "o"), ("at", "o"), ("tes", "s")] #regexp.lemmatize("amas") --> "amo"

#older reference dictionary for DictLemmatizer, works better as a standalone than lemmata
old_lemmata = open_pickle("latin-lemmatization/data/backoff/latin_lemmata_cltk.pickle")

#newer reference dictionary for DictLemmatizer, used in BackoffLemmatizer, not as good in standalone
lemmata = open_pickle("latin-lemmatization/data/backoff/latin_model.pickle")

#training data for unigram; BackoffLemmatizer randomizes it and uses some as training data
train = open_pickle("latin-lemmatization/data/backoff/latin_pos_lemmatized_sents.pickle")

#modifying training data into correct format
for l in train:
    for i in range(len(l)):
        list_tup = list(l[i])
        list_tup.pop(-1)
        l[i] = tuple(list_tup)

LatinBackoffLemmatizer._randomize_data(train=train, seed=3)
        
#-----creating default lemmatizers (CLTK Backoff & its components)--------

default = DefaultLemmatizer("/") #always returns a default lemma, used for blanks in custom pipelines
identity = IdentityLemmatizer() #returns the input as a lemma
old_diction = DictLemmatizer(lemmas=old_lemmata) #references provided "lemmas" source for exact lemma; used as last backoff in official backoff chain
diction = DictLemmatizer(lemmas=lemmata)
unigram = UnigramLemmatizer(train=train) #learns from training data to return lemmas
regexp = RegexpLemmatizer(latin_sub_patterns) #references list of replacements, runs them & returns lemma
backoff = LatinBackoffLemmatizer(verbose=False) #runs all other lemmatizer types in a chain; if any one lemmatizer returns an output, moves on. Otherwise, continues to next lemmatizer


#------------custom lemmatizers (created via utils/custom_pipeline)-----------

cltk_clone = Backoff(diction, unigram, regexp, old_diction, identity, None) #replica of CLTK Backoff Lemmatizer
cltk_simplemma = Backoff(diction, unigram, simplemma, regexp, old_diction, identity)
min_err = Backoff(diction, regexp, unigram, old_diction, identity, None)
min_err_simplemma  = Backoff(diction, regexp, unigram, old_diction, simplemma, identity)
max_correct = Backoff(unigram, old_diction, identity, None, None, None)
max_correct_simplemma = Backoff(unigram, old_diction, simplemma, identity, None, None)


#demonstrates output of above lemmatizers
def lemmatizer_example():
    backlemmatized = backoff.lemmatize(text)
    print(f"backoff: {backlemmatized}")

    unilemmatized = unigram.lemmatize(text)
    print(f"unigram: {unilemmatized}")

    old_dictlemmatized = old_diction.lemmatize(text)
    print(f"old dictionary: {old_dictlemmatized}")

    dictlemmatized = diction.lemmatize(text)
    print(f"dictionary: {dictlemmatized}")


"""These lemmatizers use the Ensemble system. Instead of a chain of lemmatizers used one-by-one as in the Backoff system, the Ensemble lemmatizers run multiple lemmatizers at once and calculates the lemma based on weighted outputs."""

eodl = EnsembleDictLemmatizer(lemmas=old_lemmata) #consults a different dictionary, more expansive but less accurate
edl = EnsembleDictLemmatizer(lemmas=lemmata, backoff=eodl) #consults a dictionary of values
eul = EnsembleUnigramLemmatizer(train=train) #uses training data to generate output, often outputs multiple possible lemmas with different weights
erl = EnsembleRegexpLemmatizer(latin_sub_patterns, backoff=edl)

#assembling the actual lemmatizer
ense = Ensemble(lem0=eodl, lem1=edl, lem2=erl, lem3=None, lem4=None, lem5=None)
