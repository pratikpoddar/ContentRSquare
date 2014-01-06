from textblob.classifiers import NaiveBayesClassifier
import articleutils

import pickledb

db = pickledb.load('url_cleaned_text.db', False) 

categories = ["Business_Finance", "Entertainment_Culture", "Environment_Weather", "Health_Medical_Pharma", "Hospitality_Recreation_Travel", "Humor_Fun", "Politics", "Religion_Social_Issues", "Sports", "Technology_Internet"]

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

def get_clean_text(url):
	if db.get(url):
		return db.get(url)
	else:
		cleaned_text = articleutils.getArticlePropertiesFromUrl(url)['cleaned_text']
		db.set(url, cleaned_text)
		db.dump()
		return cleaned_text

def createTrainingData(urls, labels):
	list_of_training_data = []
	for i in range(len(urls)):
		list_of_training_data.append((get_clean_text(urls[i]), labels[i]))
	
	return list_of_training_data
	
train = [
     ('I love this sandwich.', 'pos'),
     ('this is an amazing place!', 'pos'),
     ('I feel very good about these beers.', 'pos'),
     ('this is my best work.', 'pos'),
     ("what an awesome view", 'pos'),
     ('I do not like this restaurant', 'neg'),
     ('I am tired of this stuff.', 'neg'),
     ("I can't deal with this", 'neg'),
     ('he is my sworn enemy!', 'neg'),
     ('my boss is horrible.', 'neg')
]

cl = NaiveBayesClassifier(train)
prob_dist = cl.classify("This is an amazing library!")
print prob_dist

td = createTrainingData(["http://techcrunch.com/2013/12/30/the-twitter-nyse-honeymoon-is-over-as-stock-price-takes-another-nosedive/", "http://techcrunch.com/2013/12/29/reason-152-virtual-reality-is-awesome-personal-movie-theaters-without-the-awful-other-people/", "http://www.nytimes.com/2013/12/30/health/indias-efforts-to-aid-poor-worry-drugmakers.html?hp&_r=0", "http://www.nytimes.com/2013/12/30/nyregion/de-blasio-is-said-to-choose-schools-chancellor.html?hp"],["technology", "technology", "world", "world"])

cl = NaiveBayesClassifier(td)
prob_dist = cl.classify("India improves its health standards!")
print prob_dist

text = "Mayor de Blasio focused his inaugural address on the issue of inequality, promising that the attention he gave to the subject when he was running for office was not merely campaign rhetoric. Citing New York history embracing liberal causes, he laid out a mayoralty focused on social and economic justice. We are called to put an end to economic and social inequalities that threaten to unravel the city we love, Mr de Blasio said. And so today, we commit to a new progressive direction in New York. And that same progressive impulse has written our city history. Its in our DNA. Our work begins now, Mr de Blasio told the audience, saying he would push for the development of affordable housing, the preservation of local hospitals and the expansion of prekindergarten. For several causes, he punctuated his call for action with the words: We wont wait. Mr. de Blasio, 52, was formally sworn in shortly after midnight in a brief ceremony in front of his family rowhouse in Park Slope, Brooklyn. On the steps of City Hall later, he was ceremonially sworn in by former President Clinton, in whose administration he had served as a regional official in the Department of Housing and Urban Development. Mr. de Blasio was sworn in using a Bible once owned by Franklin Delano Roosevelt. A Democrat the new mayor begins his term as an emblem of resurgent liberalism, offering hope to progressive activists and officeholders across the country but also as an untested chief executive whose management of the city will be closely scrutinized."

text = removeNonAscii(text)



