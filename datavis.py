# External Libraries
from nltk.util import ngrams
from nltk import FreqDist
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import re

# Internal Libraries
import stopwords  # sourced from spacy

#####################################################################################################
'''Helper Functions'''
#####################################################################################################

def cleanData(text):
	'''Removes Emojis, Mentions, Hashtags, and https Hyperlinks

	Notes: 
		> strings are not being passed in implicitly, requiring convert.
		> clean all columns for NaN, nan and '' values.
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


def tokenizeText(tweets):
	'''Tokenizes text from dataframe input

	Notes: 
		> '','nan' being added weirdly.
		> Debating whether to replace contractions (i.e. isn't -> is not)
		> Edge Case: 'this--however' (em dashes) (Morgan-Stanley) [Potential Solution: Remove all Dashes]
		> NLTK impl: nltk.download('punkt'); tokens = nltk.word_tokenize(tweets) (not sure if this impl is desired)

	Parameters
	----------
	tweets : ? (some pandas type.)
		Column selection of tweets to be tokenized.

	Returns
	-------
	list
		A list of words (tokens) based on input text.
	'''

	# Split
	weird = ['', 'nan']  # '' not working, nan working
	tokens = ' '.join(t for t in tweets if t not in weird)
	tokens = tokens.split(' ')

	# Remove non-alphanumeric characters at the end or beginning of a word.
	tokens = [re.sub(r"^\W+|\W+$", "", word) for word in tokens]

	# Return
	return tokens


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
	'''

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

		Attributes
		----------
		df : pandas.core.frame.DataFrame
			Storage container for inputted container of tweets

		Raises
		------
		ValueError
			If input data is not valid. Exits program.
		'''

		# Read from DB File to DataFrame
		# conn = sqlite3.connect(f'{fileName}.db')
		# c = conn.cursor() # unnecesssary?
		# query = f'SELECT * FROM {fileName}' 
		# self.df = pd.read_sql_query(query, conn) #
		# conn.close()

		# Init Arguments
		self.fileName = fileName
		self.visualizations = visualizations.split(', ')

		# Specs
		plt.style.use('fivethirtyeight')

		# Read File
		try:
			self.df = pd.read_csv(f'output/{fileName}.csv')
			# Filter By Date (Try between_time(start, end) function?)
			self.df['post date-time'] = pd.to_datetime(self.df['post date-time'])
			if 'start_date' and 'end_date' in kwargs:
				mask = (self.df['post date-time'] >= kwargs['start_date']) & (self.df['post date-time'] <= kwargs['end_date'])
				self.df.loc[mask]
				self.df = self.df.loc[mask]
			# Sort Values By Date [Delete if Desired]
			self.df = self.df.sort_values(by='post date-time', ascending=True)
		except FileNotFoundError:
			raise ValueError  # Exits Program

		# Clean Tweets
		self.df['account status'] = self.df['account status'].apply(cleanData)
		# Visualization Calls
		modes = dict(wordCloud=self.wordCloud,
				analytics=self.analytics,
				ngrams=self.ngrams,
				polSub=self.polSub,
				valueCounts=self.valueCounts,
				freqGraph=self.freqGraph)
		# Evaluate
		for vis in self.visualizations:
			if vis in modes:
				modes[vis]()
			else:
				raise ValueError


	def preprocessing(self):
		'''Tokenize Text and Remove Stopwords'''
		tokens = tokenizeText(self.df['account status'])
		tokens = removeStopwords(tokens)
		return tokens


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
		------
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
			n = int(input("Choose n-value: "))
		else:
			n = 1

		# Clean Data Into Tokens
		tokens = self.preprocessing()

		# Generate ngram
		grams = ngrams(tokens, n)

		# Generate Frequency Distribution
		fdist = FreqDist(grams)
		freqDict = {''.join(k): v for k, v in fdist.items()}

		# Return for Internal Use
		if not userInput:
		    return freqDict

		# Otherwise, Nice Printing and Frequency Graph
		import pprint as pp
		freqDictSorted = sorted(
			freqDict.items(), key=lambda item: item[1], reverse=False)
		pp.pprint(freqDictSorted) # sorted does NOT return a dict, tuples.

		# Graph (Horizontal Bar) ...using boxplot for now, change to barh once implemented
		self.freqGraph(freqDict, 'boxplot', f"50 Most Common Phrases [n={n}]", 'output/freqDist.png',userInput=False)
		print('Image generated at output/freqDist.png')
		print('Completed ngrams.\n')


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
		# plt.imshow(wc, interpolation='bilinear')
		plt.axis('off')
		wc.to_file('output/wordCloud.png')
		print('Image generated at output/wordCloud.png')
		print('Completed wordCloud\n')


	def freqGraph(self, freqDict=None, gtype='barh', gtitle='Graph', saveloc='output/graph.png', userInput=True):
		'''Generic graphing function: plots Pie, Bar, and BoxPlots based on user Input
		The entire functionality of this function is based on a frequency dictionary.
		Therefore, allowing any type of graph with any type of data'''
		if userInput:
			print("Starting Graphing...")
			gtype = input("Choose graph type (barh, pie, boxplot): ")
			gtitle = input("Pick graph title: ")
			saveloc = 'output/graph.png'
			# Future Addition: Pick Frequency Data to Graph...give options.
			# Otherewise, just keep as an internal function.
			freqDict = self.ngrams(userInput=False) # this may vary...

		if gtype == 'barh': # WIP
			# Alan's code
			df_from_dic = pd.DataFrame(freqDict.items(), columns=["words", "count"])
			fig, ax = plt.subplots(figsize=(8,8))
			df_from_dic.iloc[0:50] # trying to get the first 50 items only
			df_from_dic.sort_values(by="count").plot.barh(
			    x='words', 
			    y='count',
			    ax=ax,
			    color='green'
			)
			# Are you able to restrict the amount of items graphed?
			# i.e. Top 50 Most Common Keywords?
		elif gtype == 'pie':
			# Alan's Code 
			pass
		elif gtype == 'boxplot':
			fig, ax = plt.subplots(figsize=(5, 5))
			plt.boxplot([v for v in freqDict.values()])

		# Show, Save, and Close Graph
		ax.set_title(gtitle)
		plt.savefig(saveloc)
		plt.clf()
		if userInput:
			print(f'Completed graphing. Figure generated at {saveloc}\n')


	def polSub(self):
		'''Plots polarity and subjectivity.
	
		Notes:
			> Requires changes to mining.py to get # values for subjectivity and sentiment.
			> WIP

		Outputs
		-------
		polSub.png
			Generated Plot of Polarity Vs. Subjectivity.
		'''

		plt.figure(figsize=(8, 6))
		for i in range(0, self.df.shape[0]):
			# scatter plot: x axis, y axis
			plt.scatter(self.df['account sentiment'],
						self.df['account subjectivity'], 
						color='Blue')

		plt.title('Sentiment Analysis')
		plt.xlabel('Sentiment')
		plt.ylabel('Subjectivity')
		plt.savefig('output/polsub.png')
		plt.clf()


	def analytics(self):
		'''Completes some general analytics.

		Notes:
			> Currently Displays Percent Positive and Negative Tweets
			> More to add in the future.
			> Maybe Rename Function
			> maybe combine valueCounts into here as well.

		Outputs
		-------
		analytics.png
			...
		'''
		print('Running Analytics...')
		postweets = self.df[self.df['account sentiment'] == 'positive']
		neuttweets = self.df[self.df['account sentiment'] == 'neutral']
		negtweets = self.df[self.df['account sentiment'] == 'negative']

		posPercent = round((postweets.shape[0] / self.df.shape[0])*100, 1)
		neutPercent = round((neuttweets.shape[0] / self.df.shape[0])*100, 1)
		negPercent = round((negtweets.shape[0] / self.df.shape[0])*100, 1)

		print(f'Percent Positive Tweets: {posPercent}%')
		print(f'Percent Neutral Tweets {neutPercent}%')
		print(f'Percent Negative Tweets: {negPercent}%')
		print('Completed Analytics.\n')


	def valueCounts(self):
		'''Prints and Plots the Counts of Postive/Negative Tweets

		Notes:
			> Requires column addition for subjectivity label.

		Outputs
		-------
		valueCounts.png
			Generated and saved to output folder.
		'''
		chart_type = input("Enter the chart type you would like for the output (Ex: bar, pie): ")

		print('Running valueCounts...')
		v = self.df['account sentiment'].value_counts()
		print(f'Value Counts: \n{v}')

		plt.title('Sentiment Analysis')
		if(chart_type == "bar"):
			# Plot and Visualize Sentiment Counts
			plt.xlabel('Sentiment')
			plt.ylabel('Counts')
			self.df['account sentiment'].value_counts().plot(kind='bar')
			plt.savefig('output/valueCounts_sentiment_bar.png')
			plt.clf()
		if(chart_type == "pie"):
			labels = 'Positive', 'Neutral', 'Negative'
			sizes = [v.positive, v.neutral, v.negative]
			colors = ['yellowgreen', 'gold', 'lightcoral']
			plt.pie(sizes, labels=labels, colors=colors,
				autopct='%1.1f%%', shadow=True, startangle=140)
			plt.savefig('output/valueCounts_sentiment_pie.png')
			plt.axis('equal')
		print('Completed valueCounts.\n')

		# Plot and Visualize Subjectivity Counts
		'''
		v = self.df['account subjectivity'].value_counts()
		print(f'Value Counts: \n{v}')
		plt.title('Subjectivity Analysis')
		plt.xlabel('Subjectivity')
		plt.ylabel('Counts')
		self.df['account subjectivity'].value_counts().plot(kind='bar')
		plt.show()
		plt.savefig('valueCounts_subjectivity.png')
		plt.clf()
		'''
