import nltk
import ssl
import re

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

# nltk.download('stopwords')

from textblob import TextBlob, Word, Blobber

def mood_function(tweet_text):
    pat = re.compile(r'[^a-zA-Z ]+')
    answer = re.sub(pat, '', tweet_text.lower())
    print(answer)
    text_obj = TextBlob(answer)
    polarity = text_obj.polarity
    subjectivity = text_obj.subjectivity

    text_obj_2 = TextBlob(tweet_text)
    polarity_2 = text_obj_2.polarity
    subjectivity_2 = text_obj_2.subjectivity

    # We can determine the thresholds for tweet mood
    mood = ""
    if polarity < -0.1:
        mood = "negative"
    elif polarity >= -0.1 and polarity <= 0.1:
        mood = "neutral"
    else:
        mood = "positive"

    mood_1 = ""
    if polarity_2 < -0.1:
        mood_1 = "negative"
    elif polarity_2 >= -0.1 and polarity_2 <= 0.1:
        mood_1 = "neutral"
    else:
        mood_1 = "positive"

    return f"textblob --> mood: {mood} ({polarity}), subjectivity level: {subjectivity}\ntextblob --> mood: {mood_1} ({polarity_2}), subjectivity level: {subjectivity_2}"