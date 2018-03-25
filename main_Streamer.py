import nltk.classify.util
from nltk.corpus import stopwords
import string
import json
import re
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import sentiment_analyser as s
import sys

 
emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
 
def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

class listener(StreamListener):

    def on_data(self, data):
        try:
            all_data = json.loads(data)
            all_tweets = all_data["text"]
            
            all_tweets = preprocess(all_tweets)

            punctuation = list(string.punctuation)

            stop_words = set(stopwords.words('english') + punctuation + ['RT'])


            tweet = [tweets for tweets in all_tweets if tweets not in stop_words]
            
            tweet = ' '.join(str(e) for e in tweet)

            sentiment_value, confidence = s.sentiment(tweet)

            print(tweet, sentiment_value, confidence)

            if confidence*100 >= 80:
                output = open("twitter-out.txt","a")
                output.write(tweet)
                output.write("\t")
                output.write(sentiment_value)
                output.write('\n')
                output.close()

			
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            return True
        return False

    def on_error(self, status):
        print(status)

tags = input('Enter the tag you want sentiment review of:')

ckey="XXXXXXXXXXXXXXXXXXXXX"
csecret="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
atoken="XXXXXXXXXXXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXXXXX"
asecret="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"


auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=[tags])
