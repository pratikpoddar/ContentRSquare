from gensim import corpora, models, similarities
from nltk.corpus import stopwords
import re
from sklearn.feature_extraction.text import TfidfVectorizer

def cleanword(word):
	return re.sub(r'\W+', '', word).strip()

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))

def crsq_unicode(s):

        if s  == None:
                return s

        if isinstance(s, unicode):
                return s
        else:
                return s.decode('utf-8')

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
	lsi = models.lsimodel.LsiModel(corpus=corp, id2word=dictionary, num_topics=30)
	return lsi

def create_sim_index(documents):
        corp = create_corpus(documents)
	index = similarities.Similarity('/tmp/tst', corp, num_features=12)
	return index

def create_tfidf(documents):
	tfidf = TfidfVectorizer().fit_transform(documents)
	sim = (tfidf * tfidf.T).A
	return sim

