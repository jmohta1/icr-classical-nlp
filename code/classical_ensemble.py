import cltk
from ensemble import *
from classical_lemma import process_text, old_lemmata, lemmata, train, text, identity

"""These lemmatizers use the Ensemble system. Instead of a chain of lemmatizers used one-by-one as in the Backoff system, the Ensemble lemmatizers run multiple lemmatizers at once and calculates the lemma based on weighted outputs."""


#----------creating the three lemmatizers that will output potential lemmas-----

edl = EnsembleDictLemmatizer(lemmas=lemmata) #consults a dictionary of values
eul = EnsembleUnigramLemmatizer(train=train, backoff=edl) #uses training data to generate output, often outputs multiple possible lemmas with different weights
#eodl = EnsembleDictLemmatizer(lemmas=old_lemmata, backoff=eul) #consults a different dictionary, more expansive but less accurate

#---------function to process & add up the weighted outputs of the lemmas-------

def lemma_weighting(word, lemmas):
    potential_lemmas = []
    for lemma in lemmas:
        for key in lemma:
            for item in lemma[key]:
                potential_lemma = item[0]
                lemma_chance = item[1]
                if key == "<EnsembleDictLemmatizer>":
                    lemma_chance /= 100
                potential_lemmas.append((potential_lemma, lemma_chance))
    weighted_lemmas = {}
    for (lemma, chance) in potential_lemmas:
        if not lemma in weighted_lemmas:
            weighted_lemmas.update({lemma:chance})
        else:
            weighted_lemmas[lemma] += chance
        
    weighted_tuples = list(weighted_lemmas.items())
    weights = [item[1] for item in weighted_tuples]
    if weights == []:
        return(identity.lemmatize([word])[0])
    else:
        lemma = weighted_tuples[weights.index(max(weights))][0]
        return((word, lemma)) 

#-------------------getting the actual lemmatization to occur-------------------

def lemmatize(text):
    output_lemmas = []
    ensemble_lemmas = eul.lemmatize(text, lemmas_only=False)
    for word, lemmas in ensemble_lemmas:
        output_lemmas.append(lemma_weighting(word, lemmas))
    return output_lemmas
