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

    return [mood, polarity, subjectivity] 

# Alternative/Merged Implementation of Clean Text
'''This implementation entirely removes hashtags and mentions'''
'''pythex.org'''
def cleanData(text, cleanEmoticons=False, removeFullHashtag=True, removeFullMention=True):
    # Removals
    if removeFullMention:
        text = re.sub(r'@[A-Za-z0-9]+','',text) # Removes mentions
    else:
        pass
    if removeFullHashtag:
        text = re.sub(r'#[A-Za-z0-9_]+','',text) # Removes hashtags
    else:
        pass
    
    text = re.sub(r'(https?)://[-a-zA-Z0-9@:%_\+.~#?&//=]*','',text) # Removes hyperlink

    # Cleanup
    text = re.sub('[\s]+',' ',text) # Removes additional white spaces
    text = text.strip('\'"').lstrip().rstrip() # Trim (Removes '' and Trailing and Leading Spaces)

    # Ref: https://gist.github.com/Alex-Just/e86110836f3f93fe7932290526529cd1#gistcomment-3208085
    # Ref: https://en.wikipedia.org/wiki/Unicode_block
    if cleanEmoticons:
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

# Subjectivity and Polarity
def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity # or t.subjectivity (the call to sentiment is really not necessary)

def getPolarity(text):
    return TextBlob(text).sentiment.polarity # or t.polarity
