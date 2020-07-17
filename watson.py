import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1
    import Features, EmotionOptions

# Authentication
authenticator = IAMAuthenticator('{apikey}')
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2019-07-12',
    authenticator=authenticator
)
natural_language_understanding.set_service_url('{url}')

#df['ibm results'] = df['tweet_text'].apply(ibm)
# Analysis
response = natural_language_understanding.analyze(text=text,
    html="<html><head><title>Fruits</title></head><body><h1>Apples and Oranges</h1><p>I love apples! I don't like oranges.</p></body></html>",
    features=Features(emotion=EmotionOptions(targets=['autonomous vehicles','crash']))).get_result()

# Printing
print(json.dumps(response, indent=2))

'''
Detects anger, disgust, fear, joy, or sadness that is 
conveyed in the content or by the context around target phrases 
specified in the targets parameter. You can analyze emotion for 
detected entities with entities.emotion and for keywords with keywords.emotion.

analyze(self, features, text=None, html=None, url=None, clean=None, xpath=None, 
fallback_to_raw=None, return_analyzed_text=None, language=None, 
limit_text_characters=None, **kwargs)
'''



import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1
    import Features, SentimentOptions

authenticator = IAMAuthenticator('{apikey}')
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2019-07-12',
    authenticator=authenticator
)

natural_language_understanding.set_service_url('{url}')

response = natural_language_understanding.analyze(
    url='www.wsj.com/news/markets',
    features=Features(sentiment=SentimentOptions(targets=['stocks']))).get_result()

print(json.dumps(response, indent=2))

'''
Analyzes the general sentiment of your content or the sentiment toward 
specific target phrases. You can analyze sentiment for detected entities 
with entities.sentiment and for keywords with keywords.sentiment .
'''