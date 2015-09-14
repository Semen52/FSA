#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Author: Angela Chapman
#  Date: 8/6/2014
#
#  This file contains code to accompany the Kaggle tutorial
#  "Deep learning goes to the movies".  The code in this file
#  is for Part 1 of the tutorial on Natural Language Processing.
#
# *************************************** #

import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from KaggleWord2VecUtility import KaggleWord2VecUtility, FuzzyWord2VecUtility
import pandas as pd
import numpy as np

if __name__ == '__main__':
    # train = pd.read_csv(os.path.join(os.path.dirname(__file__), 'data', 'labeledTrainData.tsv'), header=0, \
    #                 delimiter="\t", quoting=3)
    # test = pd.read_csv(os.path.join(os.path.dirname(__file__), 'data', 'testData.tsv'), header=0, delimiter="\t", \
    #                quoting=3 )
    train = pd.read_csv('C:\\proj\\FSA-imp\\data\\parsed\\ttk_train.tsv',
                        header=0,
                        delimiter="\t",
                        quoting=3)
    test = pd.read_csv('C:\\proj\\FSA-imp\\data\\parsed\\ttk_test_etalon.tsv',
                       header=0,
                       delimiter="\t",
                       quoting=3 )

    print 'The first review is:'
    print train["text"][0].decode('utf-8')

    raw_input("Press Enter to continue...")
    # exit(0)

    # print 'Download text data sets. If you already have NLTK datasets downloaded, just close the Python download window...'
    #nltk.download()  # Download text data sets, including stop words

    # Initialize an empty list to hold the clean reviews
    clean_train_reviews = []

    # Loop over each review; create an index i that goes from 0 to the length
    # of the movie review list

    print "Cleaning and parsing the training set movie reviews...\n"
    for i in xrange( 0, len(train["text"])):
        # clean_train_reviews.append(" ".join(KaggleWord2VecUtility.review_to_wordlist(train["text"][i], True)))
        clean_train_reviews.append(" ".join(FuzzyWord2VecUtility.text_to_wordlist(train["text"][i], True)))


    # ****** Create a bag of words from the training set
    #
    print "Creating the bag of words...\n"


    # Initialize the "CountVectorizer" object, which is scikit-learn's
    # bag of words tool.
    vectorizer = CountVectorizer(analyzer = "word",
                                 tokenizer = None,
                                 preprocessor = None,
                                 stop_words = None,
                                 max_features = 5000)
    # vocab = vectorizer.get_feature_names()
    # print vocab
    # exit(0)
    # fit_transform() does two functions: First, it fits the model
    # and learns the vocabulary; second, it transforms our training data
    # into feature vectors. The input to fit_transform should be a list of
    # strings.
    train_data_features = vectorizer.fit_transform(clean_train_reviews)

    # Numpy arrays are easy to work with, so convert the result to an
    # array
    train_data_features = train_data_features.toarray()

    # ******* Train a random forest using the bag of words
    #
    print "Training the random forest (this may take a while)..."


    # Initialize a Random Forest classifier with 100 trees
    forest = RandomForestClassifier(n_estimators = 100)

    # Fit the forest to the training set, using the bag of words as
    # features and the sentiment labels as the response variable
    #
    # This may take a few minutes to run
    forest = forest.fit( train_data_features, train["sentiment"] )



    # Create an empty list and append the clean reviews one by one
    clean_test_reviews = []

    print "Cleaning and parsing the test set movie reviews...\n"
    for i in xrange(0,len(test["text"])):
        # clean_test_reviews.append(" ".join(KaggleWord2VecUtility.review_to_wordlist(test["text"][i], True)))
        clean_test_reviews.append(" ".join(FuzzyWord2VecUtility.text_to_wordlist(test["text"][i], True)))

    # Get a bag of words for the test set, and convert to a numpy array
    test_data_features = vectorizer.transform(clean_test_reviews)
    test_data_features = test_data_features.toarray()

    # Use the random forest to make sentiment label predictions
    print "Predicting test labels...\n"
    result = forest.predict(test_data_features)

    # Copy the results to a pandas dataframe with an "id" column and
    # a "sentiment" column
    output = pd.DataFrame( data={"target":test["sentiment"], "sentiment":result} )
    print(classification_report(test["sentiment"], result))
    # Use pandas to write the comma-separated output file
    output.to_csv('C:\\proj\\FSA-imp\\results\\Bag_of_Words_model.csv', index=False, quoting=3)
    print "Wrote results to Bag_of_Words_model.csv"