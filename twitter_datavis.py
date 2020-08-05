# External Libraries
from nltk.util import ngrams
from nltk import FreqDist
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import sys
import plotly
import plotly.graph_objects as go
import plotly.express as px
from collections import Counter
from datetime import datetime
# Internal Libraries
import twitter_processing as processing



#####################################################################################################
'''Helper Functions'''
##################################################################################################### 

def displayDataframe(df):
	'''displays inputted dataframe'''
	pd.set_option("display.max_rows", None, "display.max_columns", None)
	print(df)
	pd.reset_option('all')


def exit_program(err_msg='Manual Exit'):
    '''Exits software safely'''
    print(f'\n{err_msg}')
    print("Exited program.")
    sys.exit()


def mkdir(path):
	'''Creates SubDirectories if Path Does not Exist'''
	from pathlib import Path
	Path(path).mkdir(parents=True, exist_ok=True)



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
		plt.style.use('ggplot')

		# Read File
		try:
			self.df = pd.read_csv(f'output/{fileName}.csv', parse_dates=['post date-time'], index_col='post date-time')
		except FileNotFoundError:
			exit_program('File Read Unsuccessful')  # Exits Program

		# Edit DataFrame (and sorts)
		constrain = input("\nWould you like to constrain analyzed entries? (y or n): ")
		if constrain == 'y':
			self.editDataframe()
		self.df = self.df.sort_index(ascending=True)
		self.df['datetime_extra'] = self.df.index # We dont necessarily need this. I just thought this would be helpful while indexing time.
		# print(self.df.index[0])
		print()

		# Clean DataFrame
		self.cleanDataframe()

		# Visualization Calls
		modes = dict(wordCloud=self.wordCloud,
				ngrams=self.ngrams,
				polSub=self.polSub,
				intervalGraph=self.intervalGraph,
				valueCounts=self.valueCounts,
				freqGraph=self.freqGraph,
				toneCounts=self.toneCounts,
				toneBCR=self.toneBCR,
				toneGraph=self.toneGraph,
				plotly=self.plotly)
		
		# Evaluate
		for vis in self.visualizations:
			if vis in modes:
				modes[vis]()
			else:
				exit_program(f'Visualization {vis} is not a valid input')


	def cleanDataframe(self):
		'''Cleans DataFrame.  Removes '', 'nan', and Repeat Entries'''
		total = len(self.df)
		print(f"Total Entries: {total}")
		self.df.drop_duplicates(subset='tweet id')
		print(f"***{total - len(self.df)} Duplicate Entries Removed***")
		total = len(self.df)
		self.df['account status'] = self.df['account status'].apply(processing.cleanData)
		self.df['account status'].replace('',float('nan'),inplace=True)
		self.df.dropna(subset=['account status'], inplace=True)
		print(f"***{total - len(self.df)} Empty/nan Entries Removed***")
		print(f"New Total: {len(self.df)}\n")


	def editDataframe(self):
		# Listing Options
		print("\nDataframe Editing Parameters")
		print("(1) datetime - analyze a region of tweets based on date and time")
		print("(2) sentiment - analyze a region of tweets based on sentiment")
		print("(3) subjectivity - analyze a region of tweets based on subjectivity")

		# User Selections
		valid = ('datetime', 'sentiment', 'subjectivity','tone')
		params = input("Choose Desired Parameters (Separate By Commas): ")
		params = params.split(', ')
		check = [True if p in valid else False for p in params]
		if False in check:
			exit_program('Invalid Input for Datafarme Editing Parameters')

		# Dataframe Editing
		if 'datetime' in params:
			print('Editing datetime...')
			start_date = input("Select a start date [yyyy-mm-dd hh:mm:ss] (Time is Optional): ")
			end_date = input("Select an end date [yyyy-mm-dd hh:mm:ss] (Time is Optional): ")
			self.df = self.df.loc[start_date: end_date] # start and stop of place are both included.
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
		tokens = processing.tokenizeText(self.df['account status'])
		tokens = processing.removeStopwords(tokens)
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
			> car mask
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
			> BoxPlot of sentiment score changes over time.

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
			# workaround, perhaps there's a cleaner way to do below.
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


	def intervalGraph(self, gtypes='bar, box, stacked'):
		'''Plots graphs based on intervals (boxplots, barh) of sentiment and subjectivity.

			Notes:
				> implement 'smart' interval.
				> seaborn, plotly (other libraries to consider)
				> fillna?
				> Generate all possible graphs (avoid user input)
s				> Set Interval
					self.df = self.df.sort_values(by='post date-time')
					g.iat[0]-g.iat[-1] # Timedelta('-9 days +05:45:35')
		'''
		print('*'*80)
		print('Starting intervalGraphing...')

		def openplt():
			fig = plt.figure()
			ax = plt.gca()
			return fig, ax
		def closeplt(feature, gtype):
			print(f"{gtype} graph of {feature} generated.")
			path = 'output/visuals/intervalGraph/'
			mkdir(path)
			plt.savefig(f'{path}intervalGraph_{feature}_{gtype}.png', bbox_inches='tight')
			plt.clf()

		interval = 'M'
		gtypes = gtypes.split(', ')
		
		# Form Columns
		self.df['month year'] = self.df.index.to_period(interval)
		self.df['month year'] = self.df['month year'].apply(lambda x: x.strftime('%b %Y'))
		self.df['Y'] = self.df.index.year;self.df['M'] = self.df.index.month; self.df['D'] = self.df.index.day

		if 'bar' in gtypes:
			# Sentiment
			fig,ax = openplt()
			sentmean = self.df.resample(interval)['account sentiment score'].mean()
			sentmean = sentmean.sort_index().fillna(0)
			sentmean.plot(kind='bar', ax=ax)
			ax.set(title='Sentiment Average Per Month', ylabel='Average', xlabel='Date')
			ax.set_xticklabels(sentmean.index.strftime('%b %Y').format())#,rotation=70, rotation_mode="anchor", ha="right")
			closeplt('sentiment','bar')
			# Subjectivity
			fig,ax = openplt()
			subjmean = self.df.resample(interval)['account subjectivity score'].mean()
			subjmean = subjmean.sort_index().fillna(0)
			subjmean.plot(kind='bar', ax=ax)
			ax.set(title='Subjectivity Average Per Month', ylabel='Average', xlabel='Date')
			ax.set_xticklabels(subjmean.index.strftime('%b %Y').format())#,rotation=70, rotation_mode="anchor", ha="right")
			closeplt('subjectivity','bar')
		if 'box' in gtypes:
			# Sentiment
			fig,ax = openplt()
			self.df.boxplot(by='month year', column='account sentiment score',grid=False, rot=90)
			ax.set(title='Sentiment BoxPlot Per Month', ylabel='Sentiment Score')
			closeplt('sentiment','box')
			# Subjectivity
			fig,ax = openplt()
			self.df.boxplot(by='month year', column='account subjectivity score',grid=False, rot=90)
			ax.set(title='Subjectivity BoxPlot Per Month', ylabel='Subjectivity Score')
			closeplt('subjectivity','box')
		if 'stacked' in gtypes:
			# Sentiment
			fig,ax = openplt()
			d_sent = self.df.groupby('month year').apply(lambda x: x['account sentiment'].value_counts())
			d_sent.unstack().fillna(0).plot.bar(stacked=True)
			closeplt('sentiment','stacked')
			# Subjectivity
			fig,ax = openplt()
			d = self.df.groupby('month year').apply(lambda x: x['account subjectivity'].value_counts())
			d.unstack().fillna(0).plot.bar(stacked=True) # do we really want to fillna with 0 here?
			# just remove NaN values from graph? (copy to new dataframe?)
			closeplt('subjectivity','stacked')

		# Cleanup
		self.df.drop(['Y','M','D','month year'], axis=1) # test if this is working?

		print('All output located at output/visuals/intervalGraph/')
		print('Completed intervalGraphing.')
		print('*'*80, '\n')


	def plotly(self):
		choice = input("What type of visualization do you want? \n(1) pie chart\n(2) bar graph\n(3) scatterplot\nchoice: ")
		if choice == 'pie chart':
			fig = px.sunburst(self.df, path=['user'], values='account sentiment score')
			fig.show()
		elif choice == 'bar graph':
			fig = px.bar(self.df, x="user", y=["account sentiment score", "account subjectivity score"], title="Wide-Form Input")
			fig.show()
		elif choice == 'scatterplot':
			fig = px.scatter(self.df, x='datetime_extra', y='account sentiment score')
			fig.show()
		else:
			exit_program()

		#Code to export graph as html in /output/timeStamp + choice.html - Time stamp is used to ensure output will never overwrite
		dateTimeObj = datetime.now()
		choice = "-".join(choice.split())
		timeStamp = str(dateTimeObj.year) + '-' + str(dateTimeObj.month) + '-' + str(dateTimeObj.day) + '-' + str(dateTimeObj.hour) + '-' + str(dateTimeObj.minute) + '-' + choice
		fig.write_html("output/visuals/plotly/" + timeStamp + ".html")

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
			plt.scatter(self.df['account sentiment score'],
						self.df['account subjectivity score'], # account_subjectivity score change for newer file versions. 
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

		vc_subj = self.df['account subjectivity'].value_counts()
		keys_subj = [str(k) for k in vc_subj.keys()]
		values_subj = [int(vc_subj[k]) for k in keys_subj] 
		d_subj = dict(zip(keys_subj, values_subj))
		vobjPercent = round((d_subj.get('very objective',0) / self.df.shape[0])*100, 1)
		objPercent = round((d_subj.get('objective',0) / self.df.shape[0])*100, 1)
		subjPercent = round((d_subj.get('subjective',0) / self.df.shape[0])*100, 1)
		vsubjPercent = round((d_subj.get('very subjective',0) / self.df.shape[0])*100, 1)

		# Printing
		print('SENTIMENT')
		print(f'Value Counts: \n{vc_sent}')
		print('Percentages:')
		print(f'Percent Positive Tweets: {posPercent}%')
		print(f'Percent Neutral Tweets {neutPercent}%')
		print(f'Percent Negative Tweets: {negPercent}%')
		print('SUBJECTIVITY')
		print(f'Value Counts: \n{vc_subj}')
		print('Percentages:')
		print(f'Percent Very Objective Tweets: {vobjPercent}%')
		print(f'Percent Objective Tweets {objPercent}%')
		print(f'Percent Subjective Tweets: {subjPercent}%')
		print(f'Percent Very Subjective Tweets: {vsubjPercent}')
		
		# Plotting
		sent_chart = input("Select Chart Type For Sentiment output (Ex: barh, pie): ")
		subj_chart = input("Select Chart Type For Subjectivity output (Ex: bar, pie): ")

		self.freqGraph(freqDict=d_sent, gtype=sent_chart, gtitle='Sentiment Analysis', saveloc='output/visuals/valueCounts_sentiment', userInput=False)
		self.freqGraph(freqDict=d_subj, gtype=subj_chart, gtitle='Subjectivity Analysis', saveloc='output/visuals/valueCounts_subjectivity', userInput=False)
		print('Completed valueCounts.')
		print('*'*80, '\n')


	def toneCounts(self):
		print('*'*80)
		print('Starting toneCounts')
		counts = self.df.tones.str.get_dummies(sep=', ').sum()
		print(counts)
		keys = [str(k) for k in counts.keys()]
		values = [int(counts[k]) for k in keys] 
		d = dict(zip(keys, values))
		# use another thing for size. (implement later)
		sadness = round((d.get('sadness',0) / self.df.shape[0])*100, 1)
		joy = round((d.get('joy',0) / self.df.shape[0])*100, 1)
		fear = round((d.get('fear',0) / self.df.shape[0])*100, 1)
		disgust = round((d.get('disgust',0) / self.df.shape[0])*100, 1)
		anger = round((d.get('anger',0) / self.df.shape[0])*100, 1)
		path='output/visuals/toneputs/'
		mkdir(path)
		self.freqGraph(freqDict=d, gtype='pie', gtitle='Tone Analysis', saveloc=f'{path}toneCounts', userInput=False)
		print('Completed toneCounts')
		print('*'*80,'\n')


	def toneBCR(self):
		print('*'*80)
		print('Starting toneBCR')
		from IPython.core.display import HTML
		df = self.df[['sadness_score', 'joy_score','fear_score','disgust_score','anger_score']]*100
		import bar_chart_race as bcr
		html = bcr.bar_chart_race(df,
			figsize=(4, 2.5), 
			title='Tones Over Time [0 to 1]*100',
			period_fmt='%B %d, %Y %X',
			perpendicular_bar_func='median') # add start date and end date with f-string
		path='output/visuals/toneputs/'
		mkdir(path)
		with open(f'{path}tone_barchartrace.html','w') as file:
			file.write(html.data)
		print(f'HTML file generated at {path}tone_barchartrace.html')
		print('Completed toneBCR')
		print('*'*80,'\n')


	def toneGraph(self):
		print('*'*80)
		print('Starting toneGraph...')

		# Generate Radar Graph (https://pypi.org/project/radar-chart/)
		from radar_chart.radar_chart import radar_chart
		plt.figure()
		counts = self.df.tones.str.get_dummies(sep=', ').sum()
		print(counts)
		keys = [str(k) for k in counts.keys()]
		values = [int(counts[k]) for k in keys] 
		radar_chart(values, keys, line_color='red', fill_color='red', rotate=45)
		path='output/visuals/toneputs/'
		mkdir(path)
		plt.savefig(f'{path}tone_radar.png')
		plt.clf()
		print(f'Figure generated at {path}tone_radar.png')

		# Generate BoxPlot
		plt.figure()
		self.df.boxplot(['sadness_score','joy_score','fear_score','disgust_score','anger_score'])
		plt.savefig(f'{path}tone_boxplot.png')
		plt.clf()
		print(f'Figure generated at {path}tone_boxplot.png')
		print('toneGraph complete')
		print('*'*80,'\n')
