from gensim import corpora, models, similarities
from nltk.corpus import stopwords
import re

def cleanword(word):
	return re.sub(r'\W+', '', word).strip()

def create_corpus(documents):

	# remove common words and tokenize
	stoplist = stopwords.words('english')
	stoplist.append('')
	texts = [[cleanword(word) for word in document.lower().split() if cleanword(word) not in stoplist]
        	 for document in documents]

	# remove words that appear only once
	all_tokens = sum(texts, [])
	tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)

	texts = [[word for word in text if word not in tokens_once] for text in texts]

	dictionary = corpora.Dictionary(texts)
	corp = [dictionary.doc2bow(text) for text in texts]

def create_lsi(documents):

	corp = create_corpus(documents)
	# extract 400 LSI topics; use the default one-pass algorithm
	lsi = models.lsimodel.LsiModel(corpus=corp, id2word=dictionary, num_topics=400)
	# print the most contributing words (both positively and negatively) for each of the first ten topics
	lsi.print_topics(10)

def create_sim_index(documents):
        corp = create_corpus(documents)
	index = similarities.Similarity('/tmp/tst', corp, num_features=12)
	return index
