# Twitter-Sentiment-Analysis
Live streaming of tweets from twitter streamed by the tags given by the user

# Pre-requsites
1) Tweepy
2) NLTK
3) matplotlib
4) Pickle

# What is actually happening

1) Firstly we are training out classifier for the give data set and then storing it to reduce the pre-processing time required while actually analyzing live tweets coming from twitter.
  For training we are using NaiveBayesAlgorithm.
  
2) After training the data set we pickle it into a repository name pickled_algos. We will extract our classifier and filtered data from this repository for further tasks.

3) After training and storing the data set we will start streaming the data/tweets from twitter and perform actual sentiment analysis on that data.

4) After starting the live streaming of the data we will start plotting into our dynamic graph which will keep getting updated as the streaming continues.

# How to run the Code

1) When running for the first time- Start by running Classifier_Trainer.py .You'll need to run this file only once as it will pickle your trained classifier and all the filtered data.This is done to reduce the the pre-processing time when performing actual sentiment analysis.

2) After running Classifier_Trainer.py goto the main core file i:e main_Streamer.py streaming of data happens here.
  After compiling the file Enter whatever u wanna do analysis of.When the Streaming starts your will directly get store in twitter-out.txt  file.
  While the streaming continues you can run graph.py to plot a graph of you data to know about the positivity and negativity of your tweets.
  You can stop the streaming whenever u want by pressing ctrl+c.
# P.s - Make sure you clear the Twitter-out.txt file before every new Streaming otherwise your graph will just show previous data.
#       And also make sure that you create a folder with name pickled_algos to store all your pickled data and classifier.

However the graph won't show u exact sentiments about something as people tend to tweet more when they are happy.So our graph would be more biased towards positive.
