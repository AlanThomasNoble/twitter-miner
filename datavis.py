import numpy as np 
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd # double import avoid...
import sqlite3
import re

from nltk.util import ngrams

import nltk

# How to tokenize text...replace periods with spaces...
def cleanData(text):
	# Removals
	text = re.sub(r'@[A-Za-z0-9]+','',text) # Removes mentions
	text = re.sub(r'#[A-Za-z0-9_]+','',text) # Removes hashtags
	text = re.sub(r'(https?)://[-a-zA-Z0-9@:%_\+.~#?&//=]*','',text) # Removes hyperlink
	text = re.sub('[\s]+',' ',text) # Removes additional white spaces
	text = text.strip('\'"').lstrip().rstrip() # Trim (Removes '' and Trailing and Leading Spaces)

	# Ref: https://gist.github.com/Alex-Just/e86110836f3f93fe7932290526529cd1#gistcomment-3208085
	# Ref: https://en.wikipedia.org/wiki/Unicode_block
	emoji_patterns = re.compile(
	"(["
	"\U0001F1E0-\U0001F1FF"  # flags (iOS)
	"\U0001F300-\U0001F5FF"  # symbols & pictographs
	"\U0001F600-\U0001F64F"  # emoticons
	"\U0001F680-\U0001F6FF"  # transport & map symbols
	"\U0001F700-\U0001F77F"  # alchemical symbols
	"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
	"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
	"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
	"\U0001FA00-\U0001FA6F"  # Chess Symbols
	"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
	"\U00002702-\U000027B0"  # Dingbats
	"])"
	)
	text = emoji_patterns.sub('', text)
	return text


class Visuals:
	def __init__(self, fileName, visualization, spec=''): # **kwargs
		# Read from DB File to DataFrame
		conn = sqlite3.connect(f'{fileName}.db')
		c = conn.cursor() # unnecesssary?
		query = f'SELECT * FROM {fileName}' 
		self.df = pd.read_sql_query(query, conn) # df = pandas.read_csv(f'{fileName}.csv')
		conn.close()

		# Clean Tweets (do in SQL?)
		self.df['tweet_text'] = self.df['tweet_text'].apply(cleanData)
		
		# Init Arguments
		self.fileName = fileName
		self.visualization = visualization
		self.spec = spec

		# Init Specs 
		plt.style.use('fivethirtyeight')

		# Call Visualization
		#self.ngrams(userInput=False)
		modes = dict(wordCloud=self.wordCloud)
		if visualization in modes:
			modes[visualization]()
		else:
			raise ValueError

	def phraseModeling(self):
		# bigram model that will detect frequently used phrases of two words, and stick them together
		from gensim.models.phrases import Phrases, Phraser
		tokenized_train = [t.split() for t in x_train]
		phrases = Phrases(tokenized_train)
		bigram = Phraser(phrases)

	def ngrams(self, userInput=True): # Commencing ngram analysis, how many n?, wordCloud
		userInput = False # (for now)
		if userInput:
			n = input("how many ngrams")

		# nltk.download('punkt') # REMEMBER TO DOWNLOAD WHEN RUNNING FOR FIRST TIME#
		n = 1
		tweets = (' '.join(t for t in self.df['tweet_text'])).split(' ')
		#tokens = nltk.word_tokenize(tweets)

		grams = ngrams(tweets, n)
		fdist = nltk.FreqDist(grams)
		for k,v in fdist.items():
		    print(k,v)

		return dict()

	def wordCloud(self, spec=''):
		tweets = ' '.join(t for t in self.df['tweet_text']) # [] vs generator...test, check label
		#text = self.getFrequencyDictForText(tweets)
		wc = WordCloud(width=500,height=300,max_font_size=110,random_state=21).generate(tweets) # , max_font_size=110 (200?), , random_state=21
		# wc.generate_from_frequencies(text)
		plt.imshow(wc, interpolation='bilinear')
		plt.axis('off')
		plt.show()

	def polSub(self, spec=''): # Plots Polarity and Subjectivity
		plt.figure(figsize=(8,6))
		for i in range(o, self.df.shape[0]):
			plt.scatter(self.df['Polarity'][i], self.df['Subjectivity'], color='Blue') # scatter plot: x axis, y axis

		plt.title('Sentiment Analysis')
		plt.xlabel('Polarity')
		plt.ylabel('Subjectivity')
		plt.show()

	def analytics(self, spec=''):
		ptweets = self.df[self.df.Analysis == 'Negative']
		ptweets = ptweets['Tweets']

		ntweets = self.df[self.df.Analysis == 'Negative'] # ''?
		ntweets = ntweets['Tweets']

		posPercent = round((ptweets.shape[0] / self.df.shape[0])*100, 1)
		negPercent = round((ntweets.shape[0] / self.df.shape[0])*100, 1)

		print(f'Percent Positive Tweets: {posPercent}%')
		print(f'Percent Negative Tweets: {posNegative}%')

	def valuecount(self, spec=''):
		v = self.df['Analysis'].value_counts()
		print(f'Value Counts: {v}')

		# Plot and Visualize the Counts
		plt.title('Sentiment Analysis')
		plt.xlabel('Sentiment')
		plt.ylabel('Counts')
		self.df['Analysis'].value_counts().plot(kind='bar')
		plt.show()
