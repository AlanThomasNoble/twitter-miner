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

# part of function: https://ipullrank.com/step-step-twitter-sentiment-analysis-visualizing-united-airlines-pr-crisis/
def cleanTextNN(text, cleanEmoticons=False):
    # Conversions
    text = text.lower() # Convert to lowercase
    
    # Removals
    text = re.sub(r'@[A-Za-z0-9]+','',text) # Removes mentions
    text = re.sub(r'#[A-Za-z0-9_]+','',text) # Removes hashtags
    text = re.sub(r'(https?)://[-a-zA-Z0-9@:%_\+.~#?&//=]*','',text) # Removes hyperlink

    # Cleanup
    text = re.sub('[\s]+',' ',text) # Removes additional white spaces
    text = text.strip('\'"').lstrip().rstrip() # Trim (Removes '' and Trailing and Leading Spaces)

    if cleanEmoticons:
        pass    # :\)|:-\)|:\(|:-\(|;\);-\)|:-O|8-|:P|:D|:\||:S|:\$|:@|8o\||\+o\(|\(H\)|\(C\)|\(\?\)

    return text

# # Alternative/Merged Implementation of Clean Text
# '''This implementation entirely removes hashtags and mentions'''
# '''pythex.org'''
# def cleanData(text, cleanEmoticons=False, removeFullHashtag=True, removeFullMention=True):
#     # Removals
#     if removeFullMention:
#         text = re.sub(r'@[A-Za-z0-9]+','',text) # Removes mentions
#     else:
#         pass
#     if removeFullHashtag:
#         text = re.sub(r'#[A-Za-z0-9_]+','',text) # Removes hashtags
#     else:
#         pass
    
#     text = re.sub(r'(https?)://[-a-zA-Z0-9@:%_\+.~#?&//=]*','',text) # Removes hyperlink

#     # Cleanup
#     text = re.sub('[\s]+',' ',text) # Removes additional white spaces
#     text = text.strip('\'"').lstrip().rstrip() # Trim (Removes '' and Trailing and Leading Spaces)

#     if cleanEmoticons:
#         pass    # :\)|:-\)|:\(|:-\(|;\);-\)|:-O|8-|:P|:D|:\||:S|:\$|:@|8o\||\+o\(|\(H\)|\(C\)|\(\?\)

#     return text

# Subjectivity and Polarity
def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity # or t.subjectivity (the call to sentiment is really not necessary)

def getPolarity(text):
    return TextBlob(text).sentiment.polarity # or t.polarity

# Mood Function
def mood_function(tweet_text):
    text = cleanText(tweet_text) # text_obj = TextBlob(cleanTxt(tweet_text))
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