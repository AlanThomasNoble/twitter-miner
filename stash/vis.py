import tweepy, re, pandas as pd, numpy as np 
from textblob import TextBlob
from wordcloud import WordCloud
import matlablib.pyplot as plt
plt.style.use('fivethirtyeight')

# Create a dataframe with a column called tweets.
df = pd.DataFrame([tweet.full_text for tweet in posts],columns=['Tweets'])

# Show the first five rows of data.
df.head()

# Use regex
import regex
def cleanData(text):
	text = re.sub(r'@[A-Za-z0-9]+','',text) # Removes mentions
	text = re.sub(r'#','',text) # Removing Hashtag Symbol or Remove Entire Hashtag?
	text = re.sub(r'RT[\s]+','',text) # Removing RT
	text = re.sub(r'https:\/\/\S+...regex here...','',text) # Removes hyperlink

	return text
# TODO: Emoticon Cleaning
'''
# Regex for Detecting Emoticons [Chriss Potts emoticon regex] Link str('https://www.youtube.com/watch?v=SFas7ml82NI')
# [<>]?	# optional hat/brow
# [:;=8]	# eyes
# [\-o\*\']?	# optional nose
# [\)\]\(\[dDpP/\:\}\{@\|\\]	# mouth
# |			#### reverse orientation
# [\)\]\(\[dDpP/\:\}\{@\|\\]	# mouth
# [\-o\*\']?	# optional nose
# [:;=8]	# eyes
# [<>]?	# optional hat/brow
'''

# Cleaning Text
df['Tweets']=df['Tweets'].apply(cleanTxt)

# Subjectivity and Polarity
def getSubjectivity(text):
	return TextBlob(text).sentiment.subjectivity

def getPolarity(text):
	return TextBlob(text).sentiment.polarity

# Two New Columns
df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
df['Polarity'] = df['Tweets'].apply(getPolarity)

# Word Cloud (Plotting)
allWords = ' '.join([twts for twts in df['Tweets']])
wordCloud = wordCloud(width=500,height=300, random_state=21, max_font_size=110).generate(allWords)
plt.imshow(wordCloud, interpolation=bilinear)

plt.axis('off')
plt.show()

# Negative, Neutral, and Positive Analysis
def getAnalysis(score):
	if score < 0:
		return 'Negative'
	elif score==0:
		return 'Neutral'
	else:
		return 'Positive'

df['Analysis'] = df['Polarity'].apply(getAnalysis)

# Display DataFrame
df

# Print all positive tweets
j=1
sortedDf = df.sort_values(by=['Polarity'])
for i in range(0, sortedDF.shape[0]):
	if sortedDF['Analysis'][i] == 'Positive':	
		print(f'{j}) {sortedDF['Tweet'][i]}')
		print()
		j = j + 1
print(f'{j} Postive Tweets')

# Print all Negative tweets
j=1
sortedDf = df.sort_values(by=['Polarity'], ascending=False)
for i in range(0, sortedDF.shape[0]):
	if sortedDF['Analysis'][i] == 'Negative':	
		print(f'{j}) {sortedDF['Tweet'][i]}')
		print()
		j = j + 1
print(f'{j} Negative Tweets')
# Have a UI where the user can select data models...


# Plot Polarity and Subjectivity
plt.figure(figsize=(8,6))
for in range(o, df.shape[0]):
	plt.scatter(df['Polarity'][i], df['Subjectivity'], color='Blue') # scatter plot: x axis, y axis

plt.title('Sentiment Analysis')
plt.xlabel('Polarity')
plt.ylabel('Subjectivity')
plt.show()

# Get Percentage of Positive Tweets
ptweets = df[df.Analysis == Positive]
ptweets = ptweets['Tweets']

round((ptweets.shape[0] / df.shape[0])*100, 1)

# Show Value Counts
df['Analysis'].value_counts()

# Plot and Visualize the Counts
plt.title('Sentiment Analysis')
plt.xlabel('Sentiment')
plt.ylabel('Counts')
df['Analysis'].value_counts().plot(kind='bar')
plt.show()