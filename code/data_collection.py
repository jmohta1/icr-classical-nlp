from cltk.lemmatize.backoff import *
from cltk.utils.file_operations import open_pickle
import simplemma
from classical_lemma import default, identity, old_diction, diction, unigram, regexp, backoff, process_text, Pipeline
from lemma_tester import lemma_tester
from classical_ensemble import lemmatize
from lemma_plotter import plot_lemmas

short_text = "Gallia est omnis divisa in partes tres, quarum unam incolunt Belgae, aliam Aquitani, tertiam qui ipsorum lingua Celtae, nostra Galli appellantur. Hi omnes lingua, institutis, legibus inter se differunt. Gallos ab Aquitanis Garumna flumen, a Belgis Matrona et Sequana dividit. Horum omnium fortissimi sunt Belgae, propterea quod a cultu atque humanitate provinciae longissime absunt, minimeque ad eos mercatores saepe commeant atque ea quae ad effeminandos animos pertinent important, proximique sunt Germanis, qui trans Rhenum incolunt, quibuscum continenter bellum gerunt. Qua de causa Helvetii quoque reliquos Gallos virtute praecedunt, quod fere cotidianis proeliis cum Germanis contendunt, cum aut suis finibus eos prohibent aut ipsi in eorum finibus bellum gerunt."

text = "Gallia est omnis divisa in partes tres, quarum unam incolunt Belgae, aliam Aquitani, tertiam qui ipsorum lingua Celtae, nostra Galli appellantur. Hi omnes lingua, institutis, legibus inter se differunt. Gallos ab Aquitanis Garumna flumen, a Belgis Matrona et Sequana dividit. Horum omnium fortissimi sunt Belgae, propterea quod a cultu atque humanitate provinciae longissime absunt, minimeque ad eos mercatores saepe commeant atque ea quae ad effeminandos animos pertinent important, proximique sunt Germanis, qui trans Rhenum incolunt, quibuscum continenter bellum gerunt. Qua de causa Helvetii quoque reliquos Gallos virtute praecedunt, quod fere cotidianis proeliis cum Germanis contendunt, cum aut suis finibus eos prohibent aut ipsi in eorum finibus bellum gerunt. Eorum una, pars, quam Gallos obtinere dictum est, initium capit a flumine Rhodano, continetur Garumna flumine, Oceano, finibus Belgarum, attingit etiam ab Sequanis et Helvetiis flumen Rhenum, vergit ad septentriones. Belgae ab extremis Galliae finibus oriuntur, pertinent ad inferiorem partem fluminis Rheni, spectant in septentrionem et orientem solem. Aquitania a Garumna flumine ad Pyrenaeos montes et eam partem Oceani quae est ad Hispaniam pertinet; spectat inter occasum solis et septentriones."

text = process_text(text)

errors = []
blanks = []
corrects = []
lemmatizer_labels = []

def add_lemmatizer(lemmatizer_label:str, lemmatizer, text):
    lemmatized = []
    lemmatizer_labels.append(lemmatizer_label)

    if lemmatizer_label == "Simplemma":
        for i in range(len(text)):
            lemmatized.append((text[i], simplemma.lemmatize(text[i], lang="la")))
    else:
        lemmatized = lemmatizer.lemmatize(text)
        
    results = lemma_tester(lemmatized)
    print(results)
    errors.append(results["err"])
    blanks.append(results["blank"])
    corrects.append(results["correct"])

"""
add_lemmatizer("Dict", diction, text) #undefined (inf)
add_lemmatizer("Regexp", regexp, text) #2.333
add_lemmatizer("Unigram", unigram, text) #9.12
add_lemmatizer("Simplemma", simplemma, text) #3.06
add_lemmatizer("OldDict", old_diction, text) #2.333
add_lemmatizer("Identity", identity, text) #0.83
"""

min_err = Pipeline(diction, unigram, simplemma, old_diction, identity, None)
no_simplemma = Pipeline(diction, unigram, old_diction, identity, None, None)
err_ratio = Pipeline(diction, unigram, simplemma, regexp, old_diction, identity)
err_ratio2 = Pipeline(diction, unigram, simplemma, old_diction, regexp, identity)

add_lemmatizer("Backoff", backoff, text)
add_lemmatizer("Min Error\n without Simplemma, Regexp", no_simplemma, text)
add_lemmatizer("Min Error\n without Regexp", min_err, text)
add_lemmatizer("Error Ratio", err_ratio, text)
add_lemmatizer("Error Ratio 2", err_ratio2, text)


plot_lemmas(errors, blanks, corrects, lemmatizer_labels)
