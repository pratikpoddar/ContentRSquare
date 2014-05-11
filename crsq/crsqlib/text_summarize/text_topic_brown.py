from __future__ import print_function

import numpy as np
import sys
from time import time

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.linear_model import RidgeClassifier
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import Perceptron
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.utils.extmath import density
from nltk.corpus import brown
import inspect
from crsq.crsqlib import text_summarize
from crsq.crsqlib.stringutils import *

import pickle

def get_text_topic(text):
	
	text = crsq_unicode(text)

	try:
		with open(inspect.getfile(text_summarize).replace('__init__.pyc','')+'topic_classification_brown.pickle') as f:
	        	[clf, vectorizer, target_names] = pickle.load(f)

	except Exception as e:

		vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5,
                	             stop_words='english')

		target_names = brown.categories()
		data_train = []
		data_train_target = []

		documents = [(list(brown.words(fileid)), category)
			for category in brown.categories()
		       for fileid in brown.fileids(category)]

		for doc in documents:
			data_train += [' '.join(doc[0])]
			data_train_target += [target_names.index(doc[1])]
		
		y_train = data_train_target
		X_train = vectorizer.fit_transform(data_train)
		clf = SGDClassifier(alpha=.0001, n_iter=50, penalty="l2")
		clf.fit(X_train, y_train)
        	with open(inspect.getfile(text_summarize).replace('__init__.pyc','')+'topic_classification_brown.pickle') as f:
			pickle.dump([clf, vectorizer, target_names], f)

	if text == None:
		text_data = ["No matter what has happened. No matter what you have done. No matter what you will do. I will always love you. I swear it. I wanted to tell you that wherever I am, whatever happens, I will always think of you, and the time we spent together, as my happiest time. I would do it all over again, if I had the choice. No regrets. Its one thing to fall in love. Its another to feel someone else fall in love with you, and to feel a responsibility toward that love."]
	else:
		text_data = [text]

	X_test = vectorizer.transform(text_data)
	res = clf.predict(X_test)
	return crsq_unicode(target_names[res])
	


