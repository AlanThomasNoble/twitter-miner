import numpy as np 
from wordcloud import WordCloud
import matlablib.pyplot as plt
import pandas as pd

class Visuals:
	df = []

	def vis(filename, visualization, spec=''): # **kwargs
		# Inits
		df = pandas.read_csv(file)
		plt.style.use('fivethirtyeight')

		# Call Visualization
		return visualization(df, spec)

	def wordCloud(data, spec):
		pdb.set_trace()
		tweets = ' '.join(t for t in df['Tweets']) # [] vs generator...test, check label
		wordCloud = WordCloud(width=500,height=300, random_state=21, max_font_size=110).generate(tweets)
		plt.imshow(wordCloud, interpolation=bilinear)

	def polSub(data, spec): # Plots Polarity and Subjectivity
		plt.figure(figsize=(8,6))
		for in range(o, df.shape[0]):
			plt.scatter(df['Polarity'][i], df['Subjectivity'], color='Blue') # scatter plot: x axis, y axis

		plt.title('Sentiment Analysis')
		plt.xlabel('Polarity')
		plt.ylabel('Subjectivity')
		plt.show()

	def analytics(data,spec):
		ptweets = df[df.Analysis == 'Negative']
		ptweets = ptweets['Tweets']

		ntweets = df[df.Analysis == 'Negative'] # ''?
		ntweets = ntweets['Tweets']

		posPercent = round((ptweets.shape[0] / df.shape[0])*100, 1)
		negPercent = round((ntweets.shape[0] / df.shape[0])*100, 1)

		print(f'Percent Positive Tweets: {posPercent}%')
		print(f'Percent Negative Tweets: {posNegative}%')

	def valuecount(data, spec):
		print(f'Value Counts: {df['Analysis'].value_counts()}')

		# Plot and Visualize the Counts
		plt.title('Sentiment Analysis')
		plt.xlabel('Sentiment')
		plt.ylabel('Counts')
		df['Analysis'].value_counts().plot(kind='bar')
		plt.show()
