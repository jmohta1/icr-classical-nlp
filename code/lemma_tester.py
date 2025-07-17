from cltk.lemmatize.backoff import *
from cltk.utils.file_operations import open_pickle
import simplemma
from classical_lemma import default, identity, old_diction, diction, unigram, regexp, backoff, lemma_optimizer, process_text
import json

"""For testing the lemmatizers & collecting data. Compares lemmatizers' output to a JSON file of correct lemmas."""

text1 = "quo usque tandem abutere, Catilina, patientia nostra? quam diu etiam furor iste tuus nos eludet? quem ad finem sese effrenata iactabit audacia? nihilne te nocturnum praesidium Palati, nihil urbis vigiliae, nihil timor populi, nihil concursus bonorum omnium, nihil hic munitissimus habendi senatus locus, nihil horum ora voltusque moverunt? patere tua consilia non sentis, constrictam iam horum omnium scientia teneri coniurationem tuam non vides?"

text2 = "Gallia est omnis divisa in partes tres, quarum unam incolunt Belgae, aliam Aquitani, tertiam qui ipsorum lingua Celtae, nostra Galli appellantur. Hi omnes lingua, institutis, legibus inter se differunt. Gallos ab Aquitanis Garumna flumen, a Belgis Matrona et Sequana dividit. Horum omnium fortissimi sunt Belgae, propterea quod a cultu atque humanitate provinciae longissime absunt, minimeque ad eos mercatores saepe commeant atque ea quae ad effeminandos animos pertinent important,"

text3 = "Arma virumque cano, Troiae qui primus ab oris Italiam, fato profugus, Laviniaque venit litora, multum ille et terris iactatus et alto vi superum saevae memorem Iunonis ob iram; multa quoque et bello passus, dum conderet urbem, inferretque deos Latio, genus unde Latinum, Albanique patres, atque altae moenia Romae."

#CORRECT ANSWERS JSON FILE CURRENTLY ONLY WORKS WITH text2
with open("icr-classical-nlp/data/data.json", "r") as file:
    dbg_data = json.load(file)

text = process_text(text2)
lemmatized = backoff.lemmatize(text)

punctuation = ["!", "&", "(", ")", ";", ":", ",", ".", "?", "[", "]"]



#testing system for lemmatizers; returns errors, blanks, correct, and total
def lemma_tester(lemmatized):
    err = 0
    blank = 0
    total = len(lemmatized)
    for item in lemmatized:
        if None in item:
            blank += 1
        elif item[1] in dbg_data[item[0]]:
            pass
        else:
            err += 1
    correct = total - (err+blank)
    return(f"wrong: {err}, blank: {blank}, correct: {correct}, total: {total}")


#compares two lemmatizers, outputting the differences between their lemmatization
def lemma_comparer(lemma1, lemma2):
    backlem = lemma_optimizer(list(text), diction, unigram, old_diction, identity)
    testlem = lemma_optimizer(list(text), diction, unigram, simplemma, old_diction, identity)
    differences = [] #(old, new) tuples
    for i in range(len(text)):
        if backlem[i] != testlem[i]:
            differences.append((backlem[i], testlem[i]))

    return(differences)
