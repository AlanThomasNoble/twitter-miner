import re
from textblob import TextBlob #, Word, Blobber

# function: https://ipullrank.com/step-step-twitter-sentiment-analysis-visualizing-united-airlines-pr-crisis/
def cleanTxt(tweet):
    #Convert to lower case
    tweet = tweet.lower()
    #Convert www.* or https?://* to empty str
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',tweet)
    #Convert @username to empty str
    tweet = re.sub('@[^\s]+','',tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #trim
    tweet = tweet.strip('\'"')
    return tweet

# Mood Function
def mood_function(tweet_text):
    # print(1, tweet_text)
    # print(2, cleanTxt(tweet_text))
    # print(3, cleanData(tweet_text))
    # print()
    # preprocess text and input it into textblob
    text_obj = TextBlob(cleanTxt(tweet_text))
    polarity = text_obj.polarity
    subjectivity = text_obj.subjectivity

    # We can determine the thresholds for tweet mood
    mood = ""
    if polarity < -0.01:
        mood = "negative"
    elif polarity >= -0.01 and polarity <= 0.01:
        mood = "neutral"
    else:
        mood = "positive"

    subj_level = ""
    if subjectivity <= 0.25 and subjectivity >= 0:
        subj_level = "very objective"
    elif subjectivity <= 0.5 and subjectivity > 0.25:
        subj_level = "objective"
    elif subjectivity <= 0.75 and subjectivity > 0.5:
        subj_level = "subjective"
    else:
        subj_level = "very subjective"

    return [mood, polarity, subjectivity, subj_level] 

# Subjectivity and Polarity
def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity # or t.subjectivity (the call to sentiment is really not necessary)

def getPolarity(text):
    return TextBlob(text).sentiment.polarity # or t.polarity
