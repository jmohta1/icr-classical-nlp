from cltk.lemmatize.backoff import *
from cltk.lemmatize.lat import LatinBackoffLemmatizer
from cltk.stem.lat import _checkremove_que
from cltk.text.lat import replace_jv
from cltk.utils.file_operations import open_pickle
import simplemma
import os

#functions to split text string into list of words & punct

#punctuation to be split
punctuation = ["!", "&", "(", ")", ";", ":", ",", ".", "?" "[", "]"]

def split_punct(text, punct):
    split_text = []
    for item in text:
        punct_ind = item.split(punct)
        if len(punct_ind)>1:
            
            punct_ind.insert(1, punct)
        split_text = split_text + punct_ind
    return (split_text)
            
def split_chars(text, punctuation):
    for punct in punctuation:
        text = split_punct(text, punct)
    text[:] = [word for word in text if word !=""]
    return(text)

def process_text(text):
    proc_text = text.lower()
    proc_text = replace_jv(proc_text)
    proc_text = proc_text.split(" ")
    proc_text = split_chars(proc_text, punctuation)
    proc_text = [_checkremove_que(word)[0] for word in proc_text]
    return(proc_text)

#string to be lemmatized
text = "Arma virumque cano, Troiae qui primus ab oris Italiam, fato profugus, Laviniaque venit litora, multum ille et terris iactatus et alto vi superum saevae memorem Iunonis ob iram; multa quoque et bello passus, dum conderet urbem, inferretque deos Latio, genus unde Latinum, Albanique patres, atque altae moenia Romae."

text = process_text(text)

#example for regex lemmatizer
reg = [("as", "o"), ("at", "o"), ("tes", "s")] #regexp.lemmatize("amas") --> "amo"

#older reference dictionary for DictLemmatizer, works better as a standalone than lemmata
old_lemmata = open_pickle("cltk_data/lat/model/lat_models_cltk/lemmata/backoff/latin_lemmata_cltk.pickle")

#newer reference dictionary for DictLemmatizer, used in BackoffLemmatizer, returns None often but isn't often wrong when it does output
lemmata = open_pickle("cltk_data/lat/model/lat_models_cltk/lemmata/backoff/latin_model.pickle")

#training data for unigram; BackoffLemmatizer randomizes it and uses some as training data
train = open_pickle("cltk_data/lat/model/lat_models_cltk/lemmata/backoff/latin_pos_lemmatized_sents.pickle")

#modifying training data for correct format
for l in train:
    for i in range(len(l)):
        list_tup = list(l[i])
        list_tup.pop(-1)
        l[i] = tuple(list_tup)

default = DefaultLemmatizer("custom message") #always returns a default message lemma
identity = IdentityLemmatizer() #returns the input as a lemma
old_diction = DictLemmatizer(lemmas=old_lemmata) #references provided "lemmas" source for exact lemma
diction = DictLemmatizer(lemmas=lemmata)
unigram = UnigramLemmatizer(train=train) #learns from training data to return lemmas
regexp = RegexpLemmatizer(reg) #references list of replacements, runs them & returns lemma
backoff = LatinBackoffLemmatizer(verbose=True) #runs all other lemmatizer types in a chain; if any one lemmatizer returns an output, moves on. Otherwise, continues to next lemmatizer

#testing system for lemmatizers; returns each lemmatization one by one; user types nothing for a correct answer and anything for an incorrect answer (None responses are automatically counted as blanks)
def lemma_tester(lemmatized):
    err = 0
    blank = 0
    for item in lemmatized:
        if None in list(item):
            print(item)
            blank += 1
        else:
            right = input(item)
            if right == "":
                pass
            else:
                err += 1
    print(f"wrong: {err}, blank: {blank}")
    return(err, blank)

simplemmatized = [simplemma.lemmatize(word, lang='la') for word in text]
print(f"simplemma: {simplemmatized}")
lemma_tester(simplemmatized)

backlemmatized = backoff.lemmatize(text)
print(f"backoff: {backlemmatized}")
lemma_tester(backlemmatized)

unilemmatized = unigram.lemmatize(text)
print(f"unigram: {unilemmatized}")
lemma_tester(unilemmatized)

old_dictlemmatized = old_diction.lemmatize(text)
print(f"old dictionary: {old_dictlemmatized}")
lemma_tester(old_dictlemmatized)

dictlemmatized = diction.lemmatize(text)
print(f"dictionary: {dictlemmatized}")
lemma_tester(dictlemmatized)

print(f"lemmas: {len(text)}")
