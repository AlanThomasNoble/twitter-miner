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
###################################################################################################### 
import pandas as pd
import re

def cleanData(text):
    '''Removes Mentions and Hyperlinks

    Parameters
    ----------
    text : str
        Input string to be cleaned

    Returns
    -------
    str
        String of cleaned input text
    '''

    cleaned = str(text)
    cleaned = re.sub(r'@[A-Za-z0-9]+', '', cleaned)  # Removes mentions
    cleaned = re.sub(r'((www\.[^\s]+)|(https?://[^\s]+))','',cleaned) # Removes hyperlink  
    cleaned = re.sub(r'(\bNaN\b)|(\bnan\b)','',cleaned) # Removes NaN values 
    cleaned = re.sub(r'[\s]+', ' ', cleaned)  # Removes additional white spaces
    cleaned = cleaned.strip('\'"').lstrip().rstrip() # Trim
    return cleaned

def cleanDataframe(df):
    '''Removes duplicate, nan, and empty entries from dataframe

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
        Storage container for tweets

    Returns
    -------
    df : pandas.core.frame.DataFrame
        Returns cleaned storage container.
    '''

    total = len(df)
    print(f"Total Entries: {total}")
    df.drop_duplicates(subset='tweet id', keep='first', inplace=True)
    print(f"***{total - len(df)} Duplicate Entries Removed***")
    total = len(df)
    df.dropna(subset=['account status'], inplace=True)
    print(f"***{total - len(df)} nan Entries Removed***")
    total = len(df)
    import twitter_processing as processing
    df['account status'] = df['account status'].apply(processing.cleanData)
    df['account status'].replace('',float('nan'),inplace=True)
    df.dropna(subset=['account status'], inplace=True)
    print(f"***{total - len(df)} Empty Entries Removed***")
    print(f"New Total: {len(df)}\n")
    return df

def analyze(text):
    '''Runs IBM emotion analyzer on input text. 

    Parameters
    ----------
    text : str
        Input string to be analyzed

    Returns
    -------
    list
        A list of emotion scores as well as identified tones (if expression score is > .5).
        Identitified tones are a comma separated String at index 0.
        i.e. ['sadness, joy', .83, .65, .23, .33, .15]
    '''
    
    print(f'Running Count: {analyze.counter}\r')
    analyze.counter +=1
    if text:
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
# Read File
num = 1 #### ****MODIFY HERE***** ####

file = f'keywords_output_{num}'
df = pd.read_csv(f'output/KSO/{file}.csv')

from twitter_datavis import mkdir
path = 'output/watson/'
mkdir(path)

try:
    # Clean Data
    df['account status'] = df['account status'].apply(cleanData)
    df = cleanDataframe(df)

    # Call Tone Analyzer
    analyze.counter = 1
    df[['tones', 'sadness_score', 'joy_score','fear_score','disgust_score','anger_score']] = df.apply(
        lambda row: pd.Series(analyze(row['account status'])), axis=1)

except: # Save to CSV
    df.to_csv(f'output/watson/{file}_watson.csv')

# Save to CSV
df.to_csv(f'output/watson/{file}_watson.csv')

##################################################################################################### 
'''Entire Document => Joins all tweets together and analyzes document emotion''' 
##################################################################################################### 
# Note: Text Inputs are Limited to 50000 Characters
num = 8 # Manual Input (Options 1-11)
input_file = f'output/watson/keywords_output_{num}_watson.csv'
df = pd.read_csv(input_file)
print('Starting Generation...')
try:
    text = ' '.join(df['account status'])
    print(len(text))
    import math
    units = math.ceil(len(text)/10000)
    print(f'NLU Data Units: {units}')
    import keywords
    response = natural_language_understanding.analyze(text=text,language='en', features=Features(emotion=EmotionOptions(targets=keywords.eight))).get_result()
    print(response)
except:
    import json
    with open(f'output/watson/document/entireDocumentOfTweetsResponse_{num}.txt','w') as file:
        file.write(json.dumps(response,indent=2))
        file.write(f'\n\n Character Length: {len(text)}')

import json
with open(f'output/watson/document/entireDocumentOfTweetsResponse_{num}.txt','w') as file:
    file.write(json.dumps(response,indent=2))
    file.write(f'\n\n Character Length: {len(text)}')