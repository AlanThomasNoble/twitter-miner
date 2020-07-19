# External Libraries
from nltk.util import ngrams
from nltk import FreqDist
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import re
import sys
from collections import Counter

# Internal Libraries
import stopwords  # sourced from spacy

#####################################################################################################
'''Helper Functions'''
#####################################################################################################

def cleanData(text, correctSpelling=False):
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

	# Lower text (Simplifies processing)
	text = str(text).lower()

	# Removals
	text = re.sub(r'@[A-Za-z0-9]+', '', text)  # Removes mentions
	text = re.sub(r'#([^\s]+)', r'\1', text) #Replace #word with word
	text = re.sub(r'((www\.[^\s]+)|(https?://[^\s]+))','',text) # Removes hyperlink
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
	
	# Cleanup
	text = re.sub(r'[\s]+', ' ', text)  # Removes additional white spaces
	text = text.strip('\'"').lstrip().rstrip() # Trim
	
	# Spelling Correction (https://textblob.readthedocs.io/en/dev/quickstart.html#spelling-correction)
	# Taking a really long time... to finish.
	if correctSpelling:
		from textblob import TextBlob
		text = str(TextBlob(text).correct()) 

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


def displayDataframe(df):
	'''displays current dataframe'''
	'''not tested'''
	pd.set_option("display.max_rows", None, "display.max_columns", None)
	print(df)
	pandas.reset_option('all')




#####################################################################################################
'''Visuals Class'''
#####################################################################################################

class Visuals:
	'''
	A class used to store visualization effects and analyses.
	'''

	def __init__(self, fileName, visualizations): 
		'''
		Reads file, applys specifications, and starts visualizations.

		Notes:
			> # Read from DB File to DataFrame
					conn = sqlite3.connect(f'{fileName}.db')
					c = conn.cursor() # unnecesssary?
					query = f'SELECT * FROM {fileName}' 
					self.df = pd.read_sql_query(query, conn) #
					conn.close()
		Parameters
		----------
		fileName : str
			Name of the file.
		visualizations : str
			Visualizations desired.

		Attributes
		----------
		df : pandas.core.frame.DataFrame
			Storage container for inputted container of tweets

		Raises
		------
		ValueError
			If input data is not valid. Exits program.
		'''

		# Init Arguments
		self.fileName = fileName
		self.visualizations = visualizations.split(', ') 

		# Specs
		plt.style.use('fivethirtyeight')

		# Read File
		try:
			self.df = pd.read_csv(f'output/{fileName}.csv')
			self.df['post date-time'] = pd.to_datetime(self.df['post date-time'])
		except FileNotFoundError:
			raise ValueError  # Exits Program

		# Edit DataFrame
		constrain = input("\nWould you like to constrain analyzed entries? (y or n): ")
		if constrain == 'y':
			self.editDataframe()
		self.df = self.df.sort_values(by='post date-time', ascending=True) # Sort Values By Date [Delete if Desired]

		# Clean Tweets and Correct Spellings
		self.df['account status'] = self.df['account status'].apply(cleanData)

		# Visualization Calls
		modes = dict(wordCloud=self.wordCloud,
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


	def editDataframe(self):
		# Listing Options
		print("\nDataframe Editing Parameters")
		print("(1) datetime - analyze a region of tweets based on date and time")
		print("(2) sentiment - analyze a region of tweets based on sentiment")
		print("(3) subjectivity - analyze a region of tweets based on subjectivity")

		# User Selections
		valid = ('datetime', 'sentiment', 'subjectivity')
		params = input("Choose Desired Parameters (Separate By Commas): ")
		params = params.split(', ')
		check = [True if p in valid else False for p in params]
		if False in check:
			raise ValueError # Exit Program

		# Dataframe Editing
		if 'datetime' in params:
			print('Editing datetime...')
			start_date = input("Select a start date [yyyy-mm-dd hh:mm:ss] (Time is Optional): ")
			end_date = input("Select an end date [yyyy-mm-dd hh:mm:ss] (Time is Optional): ")
			mask = (self.df['post date-time'] >= start_date) & (self.df['post date-time'] <= end_date)
			self.df = self.df.loc[mask]
		if 'sentiment' in params:
			print('Editing sentiment...')
			sentiments = input("Select Sentiments (positive, negative, neutral): ")
			sentiments = sentiments.split(', ')
			mask = (self.df['account sentiment'].isin(sentiments))
			self.df = self.df.loc[mask]
		if 'subjectivity' in params:
			print('Editing subjectivity...')
			subjs = input("Select Subjectivities (very objective, objective, subjective, very subjective): ")
			subjs = subjs.split(', ')
			mask = (self.df['account subjectivity'].isin(subjs))
			self.df = self.df.loc[mask]
		print()


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
			print('*'*80)
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
		freqDict = {', '.join(k): v for k, v in fdist.items()}

		# Return for Internal Use
		if not userInput:
		    return freqDict

		# Otherwise, Print FreqDict to File and Generate Frequency Graph
		freqDictSorted = sorted(
			freqDict.items(), key=lambda item: item[1], reverse=True)

		with open('output/ngrams_freqDict.txt', 'w') as file:
			[file.write(f'{item}\n') for item in freqDictSorted]

		print(f'List of {len(freqDict)} Entries Generated at output/ngrams_freqDict.txt')
		# Graph (Horizontal Bar)
		self.freqGraph(freqDict, 'barh', f"** Most Common Phrases [n={n}]", 'output/visuals/freqDist',userInput=False)
		print('Completed ngrams.')
		print('*'*80, '\n')


	def wordCloud(self):
		'''Generates Word Cloud based on frequency

		Notes:
			> Remove imshow() and just save image.

		Outputs
		-------
		wordCloud.png
			Generated Word Cloud.
		'''
		print('*'*80)
		print("Starting wordCloud...")
		freqDict = self.ngrams(userInput=False)
		wc = WordCloud(width=500, height=300, max_font_size=110)
		wc = wc.generate_from_frequencies(freqDict)
		# plt.imshow(wc, interpolation='bilinear')
		plt.axis('off')
		wc.to_file('output/visuals/wordCloud.png')
		print('Image generated at output/visuals/wordCloud.png')
		print('Completed wordCloud.')
		print('*'*80, '\n')


	def freqGraph(self, freqDict=None, gtype='bar', gtitle='Freq Graph', saveloc='output/visuals/freqGraph', userInput=True):
		'''Generic graphing function: generates bar, pie, and boxplot graphs based on userInput or internal funciton call.
		
		Notes:
			> Planning to shift to a purely internal function in the future.
		
		Arguments
		---------
		keyword arguments
			list of parameters to help generate the graph

		Outputs
		-------
		Desired Graph
		'''

		if userInput:
			print('*'*80)
			print("Starting Graphing...")
			gtype = input("Choose graph type (boxplot, pie, barh): ")
			freqDict = self.ngrams(userInput=False) # Future Addition: pick data to graph?

		# Automatically Limit Entries
		num = len(freqDict)
		if num > 50 and not gtype=='boxplot': # remove and not gtype=='boxplot'?
			num = 50
			print('Number Reduced to 50 for Graphing Visibility.')

		#freqDf = pd.DataFrame(list(freqDict.items()), columns=["words","count"])
		# Select Top {num} Entries
		counter_dict = Counter(freqDict)
		freqDf = pd.DataFrame(counter_dict.most_common(int(num)), columns=["words", "count"])
		freqDf = freqDf.sort_values(by='count')
		freqDict = freqDf.to_dict() # used in 'pie'

		# Init Params
		fig, ax = plt.subplots(figsize=(8,8))
		
		# Plot
		if gtype == 'barh':
			freqDf.plot.barh(
			    x='words', 
			    y='count',
			    ax=ax,
			    color='green'
			)
		elif gtype == 'boxplot':
			freqDf.boxplot()
		elif gtype == 'pie':
			data = freqDict['count'].values() 
			labels = freqDict['words'].values()
			if 'positive' in labels or 'neutral' in labels or 'negative' in labels:
				colors = ['yellowgreen', 'gold', 'lightcoral'] 
				plt.pie(data, labels=labels, colors=colors, autopct='%1.1f%%', 
					shadow=True, startangle=140)
			else:
				plt.pie(data, labels=labels, autopct='%1.1f%%', shadow=True, 
					startangle=140)
			plt.axis('equal')

		# Save and Close Graph
		ax.set_title(gtitle.replace('**', str(num)))
		plt.savefig(f'{saveloc}_{gtype}.png')
		plt.clf()

		# End
		print(f'Figure generated at {saveloc}_{gtype}.png')
		if userInput:
			print('Completed graphing')
			print('*'*80, '\n')


	def polSub(self):
		'''Plots polarity and subjectivity.
	
		Notes:
			> Requires changes to mining.py to get # values for subjectivity and sentiment.

		Outputs
		-------
		polSub.png
			Generated Plot of Polarity Vs. Subjectivity.
		'''
		print('*'*80)
		print('Running polSub...')
		plt.figure(figsize=(8, 6))
		for i in range(0, self.df.shape[0]):
			# scatter plot: x axis, y axis
			plt.scatter(self.df['account sentiment_score'],
						self.df['account subjectivity_score'], 
						color='Blue')

		plt.title('Sentiment Analysis')
		plt.xlabel('Sentiment')
		plt.ylabel('Subjectivity')
		plt.savefig('output/visuals/polsub.png')
		plt.clf()
		print('Completed polSub')
		print('*'*80, '\n')


	def valueCounts(self):
		'''Prints Counts and Percentages of Subjectivity and Polarity

		Notes:
			> Requires column addition for subjectivity label.

		Outputs
		-------
		valueCounts.png
			Generated and saved to output folder.
		'''
		print('*'*80)
		print('Running valueCounts...')
		
		# Analysis
		vc_sent = self.df['account sentiment'].value_counts()
		keys_sent = [str(k) for k in vc_sent.keys()]
		values_sent = [int(vc_sent[k]) for k in keys_sent] 
		d_sent = dict(zip(keys_sent, values_sent))
		posPercent = round((d_sent.get('positive',0) / self.df.shape[0])*100, 1)
		neutPercent = round((d_sent.get('neutral',0) / self.df.shape[0])*100, 1)
		negPercent = round((d_sent.get('negative',0) / self.df.shape[0])*100, 1)

		'''
		vc_subj = self.df['account sentiment'].value_counts()
		keys_subj = [str(k) for k in vc_subj.keys()]
		values_subj = [int(vc_subj[k]) for k in keys_subj] 
		d_subj = dict(zip(keys_subj, values))
		vobjPercent = round((d_subj.get('positive',0) / self.df.shape[0])*100, 1)
		objPercent = round((d_subj.get('positive',0) / self.df.shape[0])*100, 1)
		subjPercent = round((d_subj.get('positive',0) / self.df.shape[0])*100, 1)
		vsubjPercent = round((d_subj.get('positive',0) / self.df.shape[0])*100, 1)
		'''

		# Printing
		print('SENTIMENT')
		print(f'Value Counts: \n{vc_sent}')
		print('Percentages:')
		print(f'Percent Positive Tweets: {posPercent}%')
		print(f'Percent Neutral Tweets {neutPercent}%')
		print(f'Percent Negative Tweets: {negPercent}%')
		r'''
		print('**SUBJECTIVITY**')
		print(f'Value Counts: \n{vc_subj}')
		print('Percentages:')
		print(f'Percent Very Objective Tweets: {vobjPercent}%')
		print(f'Percent Objective Tweets {objPercent}%')
		print(f'Percent Subjective Tweets: {subjPercent}%')
		print(f'Percent Very Subjective Tweets: {vsubjPercent}')
		'''
		# Plotting
		sent_chart = input("Select Chart Type For Sentiment output (Ex: barh, pie): ")
		#subj_chart = input("Select Chart Type For Subjectivity output (Ex: bar, pie): ")

		self.freqGraph(freqDict=d_sent, gtype=sent_chart, gtitle='Sentiment Analysis', saveloc='output/visuals/valueCounts_sentiment', userInput=False)
		print('Completed valueCounts.')
		print('*'*80, '\n')

		# Plot and Visualize Subjectivity Counts
		r'''
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