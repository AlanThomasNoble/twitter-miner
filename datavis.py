from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd # double import avoid...
import sqlite3
import re

# Cleanup todo
# from nltk.util import ngrams
import nltk # eventually will want to use one library...
import spacy
import numpy as np

#####################################################################################################
'''Helper Functions'''
#####################################################################################################

# Action: Removes Emojis, Mentions, Hashtags, and https Hyperlinks
def cleanData(text):
	text = str(text).lower() # lower all text to simplify nlp later.
	# Also for some reason, strings are not being passed in implicitly.

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


# Action: Tokenizes text from a dataframe input.
# Notes:
	# > Debating whether to replace contractions (i.e. isn't -> is not)
	# > Edge Case: 'this--however' (em dashes) (Morgan-Stanley) [Potential Solution: Remove all Dashes]
	# > NLTK impl: nltk.download('punkt'); tokens = nltk.word_tokenize(tweets) (not sure if this impl is desired)
def tokenizeText(df):
	# Form list of words in all the tweets.
	tokens = (' '.join(t for t in df['account status'])).split(' ')

	# Remove any non-alphanumeric characters at the end or beginning of a word.
	tokens = [re.sub(r"^\W+|\W+$", "", word) for word in tokens]

	return tokens
'''
# https://en.wikipedia.org/wiki/Wikipedia:List_of_English_contractions
negations_dic = {"isn't":"is not", "aren't":"are not", "wasn't":"was not", "weren't":"were not",
			"haven't":"have not","hasn't":"has not","hadn't":"had not","won't":"will not",
			"wouldn't":"would not", "don't":"do not", "doesn't":"does not","didn't":"did not",
			"can't":"can not","couldn't":"could not","shouldn't":"should not","mightn't":"might not",
			"mustn't":"must not"}
'''


# Action: Removes commonly used words (stopwords).  Removes simplified web links as well (i.e. gmail.com)
# Notes:
	# > Remove any  website links as well based on domain (.com) in each token, deletes word if found
def removeStopwords(tokens):
	import stopwords # sourced from spacy
	domains = ('.com','.org','.gov','.ny','.edu') # Removes These Tokens.
	return [t for t in tokens if t not in stopwords.STOP_WORDS and t not in domains]
'''
	# https://www.ranks.nl/stopwords
	# https://gist.github.com/sebleier/554280
	# nltk might have a function for this...
	# You can generate the most recent stopword list by doing the following:
	# from nltk.corpus import stopwords
	# sw = stopwords.words("english")
	# Note that you will need to also do
	# import nltk
	# nltk.download('stopwords')
	# and download all of the corpora in order to use this.
	# This generates the most up-to-date list of 179 English words you can use. 
	# Additionally, if you run stopwords.fileids(), you'll find out what languages 
	# have available stopword lists.
'''

# Using Spacy...
# to run: df[account status_lemmatized] = df[account status].apply(lemmatizeText)
# Or, Pass in an List of 
def lemmatizeText(text):
	import spacy

	if type(text) is not list:
		text = nlp(text) # Tokenize Text if Not Already Tokenized.

	# Use a generator object LC for optimization.
	# Return
	return list(token.lemma_ for token in text)



#####################################################################################################
'''Visuals Class'''
#####################################################################################################

# Stores all Visualization Function and Data
class Visuals:
	def __init__(self, fileName, visualization, spec=''): # **kwargs
		# Read from DB File to DataFrame
		'''
		conn = sqlite3.connect(f'{fileName}.db')
		c = conn.cursor() # unnecesssary?
		query = f'SELECT * FROM {fileName}' 
		self.df = pd.read_sql_query(query, conn) #
		conn.close()
		'''

		# Read from CSV File to DataFrame
		try:
			self.df = pd.read_csv(f'output/{fileName}.csv')
		except FileNotFoundError:
			raise ValueError # Exits Program

		# Clean Tweets (Appends Additional Column) (add lemmatization)
		self.df['account status'] = self.df['account status'].apply(cleanData)
		
		# Init Arguments and Specs
		self.fileName = fileName
		self.visualization = visualization
		self.spec = spec
		plt.style.use('fivethirtyeight')

		# Call Visualization
		#self.ngrams(userInput=False)
		modes = dict(wordCloud=self.wordCloud, 
				phraseModeling=self.phraseModeling, 
				ngrams=self.ngrams)

		if visualization in modes:
			modes[visualization]()
		else:
			raise ValueError


	# Action: Prints an ngram analysis given an 'n' value (number of words in each token)
	# Notes: 
		# > Defaults to n = 1: At 1, this is essentially a frequency distribution.
		# > Might be beneficial to add an option to lemmatize text.
	def ngrams(self, userInput=True): 
		if userInput:
			n = int(input("\nHow many ngrams: ")) # should exit_program()...test.	
		else:
			n=1

		# Tokenize Text and Remove Stopwords
		tokens = tokenizeText(self.df)
		tokens = removeStopwords(tokens)

		# Generate ngram
		from nltk.util import ngrams
		grams = ngrams(tokens, n)

		# Generate Frequency Distribution
		fdist = nltk.FreqDist(grams)
		freqDict = {''.join(k):v for k,v in fdist.items()}

		# Return for Internal Use
		if not userInput:
			return freqDict

		# Otherwise, Do some Nice Printing.
		# For now...
		import pprint as pp
		freqDictSorted = sorted(freqDict.items(), key=lambda item: item[1], reverse=False)

		pp.pprint(freqDictSorted)
		fdist.plot(50, cumulative=False, title=f"50 Most Common {n}-Grams")

	# Action: Generates a WordCloud.
	# Notes:
		# > Currently working on making the algorithm base itself on frequency distribution.
	def wordCloud(self, spec=''):
		freqDict = self.ngrams(userInput=False)
		wc = WordCloud(width=500,height=300,max_font_size=110)
		wc = wc.generate_from_frequencies(freqDict)
		plt.imshow(wc, interpolation='bilinear')
		plt.axis('off')
		plt.show()

	# Action: Plots Polarity and Subjectivity
	def polSub(self, spec=''):
		plt.figure(figsize=(8,6))
		for i in range(o, self.df.shape[0]):
			plt.scatter(self.df['Polarity'][i], self.df['Subjectivity'], color='Blue') # scatter plot: x axis, y axis

		plt.title('Sentiment Analysis')
		plt.xlabel('Polarity')
		plt.ylabel('Subjectivity')
		plt.show()

	# Action: Plots some general analytics
	# Notes:
		# > Currently Displays Percent Positive and Negative Tweets
		# > More to add in the future.
	def analytics(self, spec=''):
		ptweets = self.df[self.df.Analysis == 'Negative']
		ptweets = ptweets['Tweets']

		ntweets = self.df[self.df.Analysis == 'Negative'] # ''?
		ntweets = ntweets['Tweets']

		posPercent = round((ptweets.shape[0] / self.df.shape[0])*100, 1)
		negPercent = round((ntweets.shape[0] / self.df.shape[0])*100, 1)

		print(f'Percent Positive Tweets: {posPercent}%')
		print(f'Percent Negative Tweets: {posNegative}%')

	# Maybe combine this with above ^
	def valuecount(self, spec=''):
		v = self.df['Analysis'].value_counts()
		print(f'Value Counts: {v}')

		# Plot and Visualize the Counts
		plt.title('Sentiment Analysis')
		plt.xlabel('Sentiment')
		plt.ylabel('Counts')
		self.df['Analysis'].value_counts().plot(kind='bar')
		plt.show()

	# Action: Bigram model that detercts frequently used phrase of two words and sticks them together.
	def phraseModeling(self):
		from gensim.models.phrases import Phrases, Phraser
		tokenized_train = [t.split() for t in x_train]
		phrases = Phrases(tokenized_train)
		bigram = Phraser(phrases)
