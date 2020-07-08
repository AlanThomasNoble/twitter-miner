from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
# import sqlite3
import re

# Cleanup todo
# from nltk.util import ngrams
import nltk  # eventually will want to use one library...
import spacy
import stopwords  # sourced from spacy

#####################################################################################################
'''Helper Functions'''
#####################################################################################################

def cleanData(text):
	'''Removes Emojis, Mentions, Hashtags, and https Hyperlinks

	Notes: 
		> strings are not being passed in implicitly, requiring convert.

	Parameters
	----------
	text : str
		Input string to be cleaned

	Returns
	-------
	str
		String of cleaned input text
	'''

	text = str(text).lower()  # Lowers text (Simplifies processing)

	# Removals
	text = re.sub(r'@[A-Za-z0-9]+', '', text)  # Removes mentions
	text = re.sub(r'#[A-Za-z0-9_]+', '', text)  # Removes hashtags
	text = re.sub(r'(https?)://[-a-zA-Z0-9@:%_\+.~#?&//=]*', '', text) # Removes hyperlink
	text = re.sub('[\s]+', ' ', text)  # Removes additional white spaces
	text = text.strip('\'"').lstrip().rstrip() # Trim

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

	# Return
	text = emoji_patterns.sub('', text)
	return text


def tokenizeText(df):
	'''Tokenizes text from dataframe input

	Notes: 
		> '','nan' being added weirdly.
		> Debating whether to replace contractions (i.e. isn't -> is not)
		> Edge Case: 'this--however' (em dashes) (Morgan-Stanley) [Potential Solution: Remove all Dashes]
		> NLTK impl: nltk.download('punkt'); tokens = nltk.word_tokenize(tweets) (not sure if this impl is desired)

	Parameters
	----------
	df : pandas.core.frame.DataFrame
		Storage container for inputted csv file.

	Returns
	-------
	list
		A list of words (tokens) based on input text.
	'''

	# Split
	weird = ['', 'nan']  # '' not working, nan working
	tokens = ' '.join(t for t in df['account status'] if t not in weird)
	tokens = tokens.split(' ')

	# Remove non-alphanumeric characters at the end or beginning of a word.
	tokens = [re.sub(r"^\W+|\W+$", "", word) for word in tokens]

	# Return
	return tokens

'''
# https://en.wikipedia.org/wiki/Wikipedia:List_of_English_contractions
negations_dic = {"isn't":"is not", "aren't":"are not", "wasn't":"was not", "weren't":"were not",
			"haven't":"have not","hasn't":"has not","hadn't":"had not","won't":"will not",
			"wouldn't":"would not", "don't":"do not", "doesn't":"does not","didn't":"did not",
			"can't":"can not","couldn't":"could not","shouldn't":"should not","mightn't":"might not",
			"mustn't":"must not"}
'''


def removeStopwords(tokens):
	'''Removes common words (stopwords) and simple web links.

	Notes:

	Parameters
	----------
	tokens : str
		The sound the animal makes (default is None)

	Returns
	-------
	list
		A list of words with stopwords removed.
	'''

	domains = ('.com', '.org', '.gov', '.ny', '.edu')
	return [t for t in tokens if t not in stopwords.STOP_WORDS and not t.endswith(domains)]


def expandAbbr(tokens):
	'''Expands common twitter abbreviations to full text.

	Notes:
		> Make function similar to removeStopwords()
		> Create a file of abbreviations, abbrs.py
		> import abbrs

	Parameters
	----------
	tokens : str
		A list of words (str)

	Returns
	-------
	list
		A list of words with abbreviations expanded.
	'''

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


def lemmatizeText(tokens):
	'''Removes common words (stopwords) and simple web links.

	Notes:
		> WIP
		> Figure out how to pass in a list of words.
		> Add feature to expand twitter abbreviations (maybe this is another function)

	Parameters
	----------
	tokens : list
		A list of words (str)

	Returns
	-------
	list
		A list of words with each word lemmatized, if applicable.
	'''

	# This function is still a WIP...
	import spacy

	if type(text) is not list:
		text = nlp(text) # tokenizes text..again.

	# Return
	return list(token.lemma_ for token in text)




#####################################################################################################
'''Visuals Class'''
#####################################################################################################

class Visuals:
	'''
	A class used to store visualization effects and analyses.

	Attributes
	----------
	df : pandas.core.frame.DataFrame
		Storage container for inputted container of tweets
	'''

	df = None

	def __init__(self, fileName, visualizations, **kwargs): 
		'''
		Reads file, applys specifications, and starts visualizations.

		Parameters
		----------
		fileName : str
			Name of the file.
		visualizations : str
			Visualizations desired.
		**kwargs : multiple, optional
			Additional Specifications.

		Raises
		----------
		ValueError
			If input data is not valid. Exits program.
		'''

		# Read from DB File to DataFrame
		# conn = sqlite3.connect(f'{fileName}.db')
		# c = conn.cursor() # unnecesssary?
		# query = f'SELECT * FROM {fileName}' 
		# df = pd.read_sql_query(query, conn) #
		# conn.close()

		# Read File
		try:
			df = pd.read_csv(f'output/{fileName}.csv')
		except FileNotFoundError:
			raise ValueError  # Exits Program

		# Clean Tweets
		df['account status'] = df['account status'].apply(cleanData)

		# Init Arguments
		self.fileName = fileName
		self.visualizations = visualizations.split(', ')

		# Specs
		plt.style.use('fivethirtyeight')

		# Visualization Calls
		modes = dict(wordCloud=self.wordCloud,
				phraseModeling=self.phraseModeling,
				ngrams=self.ngrams,
				lemmas=self.lemmas,
				polSub=self.polSub,
				valueCounts=self.valueCounts)
		# Evaluate
		for vis in self.visualizations:
			if vis in modes:
				modes[vis]()
			else:
				raise ValueError


	def ngrams(self, userInput=True):
		'''Prints an ngram analysis given an 'n' value. Defaults to n=1

		Notes:
			> Defaults to n = 1: At 1, this is essentially a frequency distribution.
			> Figure a simpler/better way to print and plot data nicely
			> Check if program is exited nicely.

		Parameters
		----------
		tokens : list
			A list of words (str)
		
		Raises
		----------
		ValueError
			If input data is not valid. Exits program.

		Returns
		-------
		list
			A list of words with each word lemmatized, if applicable.

		Outputs
		-------
		freqDist.png
			Generated frequency distribution plot if userInput=False
		'''

		# User Input
		if userInput:
			print("Starting ngrams...")
			# should exit_program()...test.
			n = int(input("\nChoose n-value: "))
		else:
			n = 1

		# Tokenize Text and Remove Stopwords
		tokens = tokenizeText(df)
		tokens = removeStopwords(tokens)

		# Generate ngram
		from nltk.util import ngrams
		grams = ngrams(tokens, n)

		# Generate Frequency Distribution
		fdist = nltk.FreqDist(grams)
		freqDict = {''.join(k): v for k, v in fdist.items()}

		# Return for Internal Use
		if not userInput:
		    return freqDict

		# Otherwise, Nice Printing and Frequency Graph
		import pprint as pp
		freqDictSorted = sorted(
			freqDict.items(), key=lambda item: item[1], reverse=False)

		pp.pprint(freqDictSorted)
		plt.ion()
		fdist.plot(50, cumulative=False,
					title=f"50 Most Common Phrases [n={n}]")
		plt.savefig('output/freqDist.png')
		plt.ioff()
		plt.show()
		plt.clf()
		print('\nCompleted ngrams. Figure generated at output/freqDist.png')


	def wordCloud(self):
		'''Generates Word Cloud based on frequency

		Notes:
			> Remove imshow() and just save image.

		Outputs
		-------
		wordCloud.png
			Generated Word Cloud.
		'''

		print("Starting wordCloud...")
		freqDict = self.ngrams(userInput=False)
		wc = WordCloud(width=500, height=300, max_font_size=110)
		wc = wc.generate_from_frequencies(freqDict)
		plt.imshow(wc, interpolation='bilinear')
		plt.axis('off')
		plt.savefig('output/wordCloud.png')
		plt.clf()
		print('\nImage generated at output/wordCloud.png')


	def polSub(self):
		'''Plots polarity and subjectivity.

		Notes:
			> WIP

		Outputs
		-------
		polSub.png
			Generated Plot of Polarity Vs. Subjectivity.
		'''
		plt.figure(figsize=(8, 6))
		for i in range(0, df.shape[0]):
			# scatter plot: x axis, y axis
			plt.scatter(df['account sentiment'][i],
						df['account subjectivity'], 
						color='Blue')

		plt.title('Sentiment Analysis')
		plt.xlabel('Sentiment/Polarity')
		plt.ylabel('Subjectivity')
		# plt.show()
		plt.imshow()


	def analytics(self, spec=''):
		'''Completes some general analytics.

		Notes:
			> Currently Displays Percent Positive and Negative Tweets
			> More to add in the future.

		Outputs
		-------
		analytics.png
			...
		'''

		ptweets = df[df.Analysis == 'Negative']
		ptweets = ptweets['Tweets']

		ntweets = df[df.Analysis == 'Negative']  # ''?
		ntweets = ntweets['Tweets']

		posPercent = round((ptweets.shape[0] / df.shape[0])*100, 1)
		negPercent = round((ntweets.shape[0] / df.shape[0])*100, 1)

		print(f'Percent Positive Tweets: {posPercent}%')
		print(f'Percent Negative Tweets: {posNegative}%')


	def valueCounts(self):
		'''Prints and Plots the Counts of Postive/Negative Tweets

		Notes:
			> WIP
			> Add account subjectivity

		Outputs
		-------
		valueCounts.png
			Generated...
		'''
		v = df['account sentiment'].value_counts()
		print(f'Value Counts: {v}')

		# Plot and Visualize the Counts
		plt.title('Sentiment Analysis')
		plt.xlabel('Sentiment')
		plt.ylabel('Counts')
		df['account sentiment'].value_counts().plot(kind='bar')
		plt.show()


	def phraseModeling(self):
		'''Bigram model, detects frequently used two word phrases.

		Notes:
			> Based on gensim model.
			> Not tested, might use as an alternative method.

		'''
		from gensim.models.phrases import Phrases, Phraser
		tokenized_train = [t.split() for t in x_train]
		phrases = Phrases(tokenized_train)
		bigram = Phraser(phrases)