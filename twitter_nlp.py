# import nltk
# import ssl
import re
# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

# nltk.download()

from textblob import TextBlob #, Word, Blobber

# copied a clean txt function: https://ipullrank.com/step-step-twitter-sentiment-analysis-visualizing-united-airlines-pr-crisis/
'''
def cleanTxt(tweet):
    #Convert to lower case
    tweet = tweet.lower()
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
    #Convert @username to AT_USER
    tweet = re.sub('@[^\s]+','AT_USER',tweet)
    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #trim
    tweet = tweet.strip('\'"')
    return tweet  
'''

# Alternative/Merged Implementation of Clean Text
'''This implementation entirely removes hashtags and mentions'''
'''pythex.org'''
def cleanData(text, cleanEmoticons=False, removeFullHashtag=True, removeFullMention=True):
    # Removals
    if removeFullMention:
        text = re.sub(r'@[A-Za-z0-9]+','',text) # Removes mentions
    else:
        # use above cleanTxt
    if removeFullHashtag:
        text = re.sub(r'#[A-Za-z0-9_]+','',text) # Removes hashtags
    else:
        # use above cleanTxt
    text = re.sub(r'(https?)://[-a-zA-Z0-9@:%_\+.~#?&//=]*','',text) # Removes hyperlink

    # Cleanup
    text = re.sub('[\s]+',' ',text) # Removes additional white spaces
    text = text.strip('\'"').lstrip().rstrip() # Trim (Removes '' and Trailing and Leading Spaces)

    if cleanEmoticons:
        pass    # :\)|:-\)|:\(|:-\(|;\);-\)|:-O|8-|:P|:D|:\||:S|:\$|:@|8o\||\+o\(|\(H\)|\(C\)|\(\?\)

    return text

# Subjectivity and Polarity
def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity # or t.subjectivity (the call to sentiment is really not necessary)

def getPolarity(text):
    return TextBlob(text).sentiment.polarity # or t.polarity

# Mood Function
def mood_function(tweet_text):
    text = cleanData(tweet_text) # text_obj = TextBlob(cleanTxt(tweet_text))
    polarity = getSubjectivity(text) #text_obj.polarity
    subjectivity = getPolarity(text) #text_obj.subjectivity

    # We can determine the thresholds for tweet mood
    mood = ""
    if polarity < -0.01:
        mood = "negative"
    elif polarity >= -0.01 and polarity <= 0.01:
        mood = "neutral"
    else:
        mood = "positive"

    return [mood, polarity, subjectivity]