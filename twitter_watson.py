##################################################################################################### 
'''Authentication'''
#####################################################################################################
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions
url = 'https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/01819b6d-b49b-4d11-8f72-5bb0e2f0d012'
api_key = 'bE7fCcXqMVlWEul6-be9bLCug5bB8qBiFiX_j4mr6CkO'
# Authentication
authenticator = IAMAuthenticator(api_key)
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2019-07-12',
    authenticator=authenticator
)
natural_language_understanding.set_service_url(url)

##################################################################################################### 
'''Processing Function'''
#############################-######################################################################## 
import pandas as pd
import re

def cleanData(text):
    cleaned = str(text)
    cleaned = re.sub(r'@[A-Za-z0-9]+', '', cleaned)  # Removes mentions
    cleaned = re.sub(r'((www\.[^\s]+)|(https?://[^\s]+))','',cleaned) # Removes hyperlink  
    cleaned = re.sub(r'(\bNaN\b)|(\bnan\b)','',cleaned) # Removes NaN values 
    cleaned = re.sub(r'[\s]+', ' ', cleaned)  # Removes additional white spaces
    cleaned = cleaned.strip('\'"').lstrip().rstrip() # Trim
    return cleaned

def analyze(text):
    print(f'Running Count: {analyze.counter}\r')
    analyze.counter +=1
    if text: # Error Occurs if Empty Text is Passed In
        response = natural_language_understanding.analyze(text=text,language='en', features=Features(emotion=EmotionOptions())).get_result()
        sadness = response['emotion']['document']['emotion']['sadness']
        joy = response['emotion']['document']['emotion']['joy']
        fear = response['emotion']['document']['emotion']['fear']
        disgust = response['emotion']['document']['emotion']['disgust']
        anger = response['emotion']['document']['emotion']['anger']
        scores = [sadness, joy, fear, disgust, anger]
        names = ['sadness','joy','fear','disgust','anger']
        group = list(zip(scores,names))
        tones = list(map(lambda name: name[1], filter(lambda scores: scores[0] > .5, group)))
        tones = ', '.join(tones)
        scores.insert(0, tones)
        return scores

    NaN = float('NaN') # workaround
    return [None,NaN,NaN,NaN,NaN,NaN]

##################################################################################################### 
'''Read File, Call Functions, Save to CSV File'''
##################################################################################################### 
file = 'KEYWORD_SEARCH_OUTPUT'
df = pd.read_csv(f'output/{file}.csv')

# Call Functions
df['account status'] = df['account status'].apply(cleanData)
df['account status'].replace('',float('nan'),inplace=True)
df.dropna(subset=['account status'], inplace=True)
analyze.counter = 1
df[['tones', 'sadness_score', 'joy_score','fear_score','disgust_score','anger_score']] = df.apply(
    lambda row: pd.Series(analyze(row['account status'])), axis=1)

df.to_csv(f'{file}_watson.csv')

##################################################################################################### 
'''Entire Document (I think we may be limited by the size of the text input (But hopefully we should be fine)''' 
##################################################################################################### 
# Check out Datavis.py
text = ' '.join(df['account status'])
response = natural_language_understanding.analyze(text=text,language='en', features=Features(emotion=EmotionOptions(targets=['Covid-19','Autonomous Vehicles']))).get_result()
print(response)

import json
with open('entireDocumentOfTweetsResponse.txt','w') as file:
    file.write(json.dumps(response,indent=2))