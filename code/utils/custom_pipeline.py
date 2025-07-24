class Pipeline:
    def __init__(self, lem0, lem1, lem2, lem3, lem4, lem5):
            self.lem0 = lem0
            self.lem1 = lem1
            self.lem2 = lem2
            self.lem3 = lem3
            self.lem4 = lem4
            self.lem5 = lem5
            self.lems =  [self.lem0, self.lem1, self.lem2, self.lem3, self.lem4, self.lem5]
            lemcopy = self.lems.copy()
            for item in lemcopy:
                if item == None:
                    self.lems.remove(item)
                                
class Backoff(Pipeline):
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

#When making a custom Ensemble group, enter the lemmatizer with no backoff as lem0 and continue up the backoff chain from there

class Ensemble(Pipeline):
    
    def lemma_weighting(self, word, lemmas):
        potential_lemmas = []
        for lemma in lemmas:
            for key in lemma:
                for item in lemma[key]:
                    potential_lemma = item[0]
                    potential_lemma = potential_lemma.strip("1")
                    potential_lemma = potential_lemma.strip("2")
                    potential_lemma = potential_lemma.strip("3")
                    potential_lemma = potential_lemma.strip("4")
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
            return((word, None))
        else:
            lemma = weighted_tuples[weights.index(max(weights))][0]
            return((word, lemma))
        
    def lemmatize(self, text):
        output_lemmas = []
        ensemble_lemmas = self.lems[-1].lemmatize(text, lemmas_only=False)
        for word, lemmas in ensemble_lemmas:
            output_lemmas.append(self.lemma_weighting(word, lemmas))
        return output_lemmas
