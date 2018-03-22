from nltk.tokenize import sent_tokenize, word_tokenize
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews,stopwords
import pickle
import gzip
import random
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
import string



document = []
short_pos = open("positive.txt","r").read()
short_neg = open("negative.txt","r").read()


for r in short_pos.split('\n'):
    document.append( (r, "pos") )

for r in short_neg.split('\n'):
    document.append( (r, "neg") )

save_doc = open("pickled_algos/documents.pickle", "wb")
pickle.dump(document, save_doc)
save_doc.close()


all_words = []

short_pos_words = word_tokenize(short_pos)
short_neg_words = word_tokenize(short_neg)

for w in short_pos_words:
    all_words.append(w.lower())

for w in short_neg_words:
    all_words.append(w.lower())

punctuation = list(string.punctuation)

stop_words = set(punctuation)

all_words = nltk.FreqDist(all_words)

word_features = list(all_words.keys())[:5000]

save_doc = open("pickled_algos/word_features.pickle", "wb")
pickle.dump(word_features,save_doc)
save_doc.close()

def find(documents):
    temp = {}
    word = word_tokenize(documents)
    n = 2
    score_fn=BigramAssocMeasures.chi_sq

    bigram_finder = BigramCollocationFinder.from_words(word)
    bigrams = bigram_finder.nbest(score_fn, n)
    
    for w in word_features:
        temp[w] = (w in word )
    for w in bigrams:
        temp[w] = True
        
    return temp

features = [(find(w) , ids) for (w , ids) in document]

training_set = features[:4600] + features[5000:10300]
testing_set = features[4600:5000] + features[10300:]


classifier = NaiveBayesClassifier.train(training_set)
classify_buffer = open("pickled_algos/classifier.pickle", 'wb')
pickle.dump(classifier, classify_buffer)
classify_buffer.close()

print("Classifier accuracy percent:",(nltk.classify.accuracy(classifier, testing_set))*100)

classifier.show_most_informative_features(15)
