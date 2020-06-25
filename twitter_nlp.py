import nltk
import ssl

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

# nltk.download('stopwords')

from textblob import TextBlob, Word, Blobber

def mood_function(tweet_text):
    text_obj = TextBlob(tweet_text)
    polarity = text_obj.polarity
    subjectivity = text_obj.subjectivity

    # We can determine the thresholds for tweet mood
    mood = ""
    if polarity < -0.1:
        mood = "negative"
    elif polarity >= -0.1 and polarity <= 0.1:
        mood = "neutral"
    else:
        mood = "positive"

    return f"mood: {mood} ({polarity}), subjectivity level: {subjectivity}"