import nltk
import random
import pickle
from nltk.classify import ClassifierI
from nltk.tokenize import word_tokenize
from statistics import mode
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures

class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf

l_d = open("pickled_algos/documents.pickle", "rb")
documents = pickle.load(l_d)
l_d.close()

w_features = open("pickled_algos/word_features.pickle", "rb")
word_features = pickle.load(w_features)
w_features.close()

def find(documents):
    temp = {}
    word = set(documents)
    n = 2
    score_fn=BigramAssocMeasures.chi_sq

    bigram_finder = BigramCollocationFinder.from_words(word)
    bigrams = bigram_finder.nbest(score_fn, n)
    
    for w in word_features:
        temp[w] = (w in word )
    for w in bigrams:
        temp[w] = True
        
    return temp

classify_buffer = open("pickled_algos/classifier.pickle", "rb")
classifier = pickle.load(classify_buffer)
classify_buffer.close()

def sentiment(text):
    feat = find(text)
    return VoteClassifier(classifier).classify(feat),VoteClassifier(classifier).confidence(feat)
