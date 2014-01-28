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

import pickle


try:
	with open('topic_classification_brown.pickle') as f:
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
        with open('topic_classification_brown.pickle', 'w') as f:
		pickle.dump([clf, vectorizer, target_names], f)

text_data = ["Sachin Tendulkar is a great cricketeer. Sachin Ramesh Tendulkar (born 24 April 1973) is an Indian former cricketer widely acknowledged as the greatest batsman of the modern generation, popularly holds the title 'God of Cricket' among his fans. He is also acknowledged as the greatest cricketer of all time. He took up cricket at the age of eleven, made his Test debut against Pakistan at the age of sixteen, and went on to represent Mumbai domestically and India internationally for close to twenty-four years. He is the only player to have scored one hundred international centuries, the first batsman to score a Double Century in a One Day International, and the only player to complete more than 30,000 runs in international cricket.[10] In October 2013, he became the 16th player and first Indian to aggregate 50,000 runs in all recognized cricket (First-class, List A and Twenty20 combined). In 2002, Wisden Cricketers' Almanack ranked him the second greatest Test batsman of all time, behind Don Bradman, and the second greatest ODI batsman of all time, behind Viv Richards.[14] Later in his career, Tendulkar was a part of the Indian team that won the 2011 World Cup, his first win in six World Cup appearances for India.[15] He had previously been named 'Player of the Tournament' at the 2003 edition of the tournament, held in South Africa. In 2013, he was the only Indian cricketer included in an all-time Test World XI named to mark the 150th anniversary of Wisden Cricketers' Almanack"]

text_data = ["No matter what has happened. No matter what you have done. No matter what you will do. I will always love you. I swear it. I wanted to tell you that wherever I am, whatever happens, I will always think of you, and the time we spent together, as my happiest time. I would do it all over again, if I had the choice. No regrets. Its one thing to fall in love. Its another to feel someone else fall in love with you, and to feel a responsibility toward that love."]

X_test = vectorizer.transform(text_data)
res = clf.predict(X_test)
print(target_names[res])


