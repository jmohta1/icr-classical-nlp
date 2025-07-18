from cltk.lemmatize.backoff import *
from cltk.lemmatize.lat import LatinBackoffLemmatizer
from cltk.stem.lat import _checkremove_que
from cltk.text.lat import replace_jv
from cltk.utils.file_operations import open_pickle
from cltk.lemmatize.lat import latin_sub_patterns
import simplemma

#---------processing text--------------

punctuation = ["!", "&", "(", ")", ";", ":", ",", ".", "?", "[", "]"]

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
#-----------------------------------------


#string to be lemmatized
text = "quo usque tandem abutere, Catilina, patientia nostra? quam diu etiam furor iste tuus nos eludet? quem ad finem sese effrenata iactabit audacia? nihilne te nocturnum praesidium Palati, nihil urbis vigiliae, nihil timor populi, nihil concursus bonorum omnium, nihil hic munitissimus habendi senatus locus, nihil horum ora voltusque moverunt? patere tua consilia non sentis, constrictam iam horum omnium scientia teneri coniurationem tuam non vides?"

text = process_text(text)

#-------------training/reference data----------------

#example regular expressions for regex lemmatizer
reg = [("as", "o"), ("at", "o"), ("tes", "s")] #regexp.lemmatize("amas") --> "amo"

#older reference dictionary for DictLemmatizer, works better as a standalone than lemmata
old_lemmata = open_pickle("icr-classical-nlp/data/backoff/latin_lemmata_cltk.pickle")

#newer reference dictionary for DictLemmatizer, used in BackoffLemmatizer, not as good in standalone
lemmata = open_pickle("icr-classical-nlp/data/backoff/latin_model.pickle")

#training data for unigram; BackoffLemmatizer randomizes it and uses some as training data
train = open_pickle("icr-classical-nlp/data/backoff/latin_pos_lemmatized_sents.pickle")

#modifying training data into correct format
for l in train:
    for i in range(len(l)):
        list_tup = list(l[i])
        list_tup.pop(-1)
        l[i] = tuple(list_tup)

#-----------creating lemmatizers--------------

default = DefaultLemmatizer("custom lemma") #always returns a default lemma
identity = IdentityLemmatizer() #returns the input as a lemma
old_diction = DictLemmatizer(lemmas=old_lemmata) #references provided "lemmas" source for exact lemma; used as last backoff in official backoff chain
diction = DictLemmatizer(lemmas=lemmata)
unigram = UnigramLemmatizer(train=train) #learns from training data to return lemmas
regexp = RegexpLemmatizer(latin_sub_patterns) #references list of replacements, runs them & returns lemma
backoff = LatinBackoffLemmatizer(verbose=False) #runs all other lemmatizer types in a chain; if any one lemmatizer returns an output, moves on. Otherwise, continues to next lemmatizer

#----------------------------------------------

class Pipeline:
    def __init__(self, lem0, lem1, lem2, lem3, lem4, lem5):
            self.lem0 = lem0
            self.lem1 = lem1
            self.lem2 = lem2
            self.lem3 = lem3
            self.lem4 = lem4
            self.lem5 = lem5
            self.lems =  [self.lem0, self.lem1, self.lem2, self.lem3, self.lem4, self.lem5]
            for item in self.lems:
                if item == None:
                    self.lems.remove(item)
                
            
    def lemmatize(self, text):
        finished_lems = list(text)
        for i in range(len(text)):
            for lemmatizer in self.lems:
                try:
                    lemmatized = lemmatizer.lemmatize([text[i]])
                except TypeError:
                    lemmatized = [(text[i], lemmatizer.lemmatize(text[i], lang="la"))]
                if lemmatized[0][1] != None:
                    finished_lems[i] = lemmatized[0]
                    break
        return(finished_lems)
                

#demonstrates output of lemmatizers
def lemmatizer_example():
    backlemmatized = backoff.lemmatize(text)
    print(f"backoff: {backlemmatized}")

    unilemmatized = unigram.lemmatize(text)
    print(f"unigram: {unilemmatized}")

    old_dictlemmatized = old_diction.lemmatize(text)
    print(f"old dictionary: {old_dictlemmatized}")

    dictlemmatized = diction.lemmatize(text)
    print(f"dictionary: {dictlemmatized}")
