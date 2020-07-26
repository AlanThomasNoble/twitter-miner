api_key = '7fkZR-pGDwaZ9ly06zP3gVVaAOKnk-JXCPNwBVvRIELi'
url = 'https://api.eu-de.tone-analyzer.watson.cloud.ibm.com/instances/015059dd-f5b7-4452-930a-332ef776ff7e'

from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator(api_key)
tone_analyzer = ToneAnalyzerV3(
    version='2017-09-21',
    authenticator=authenticator
)
tone_analyzer.set_service_url(url)

def cleanData(text):
	cleaned = str(text)
	cleaned = re.sub(r'@[A-Za-z0-9]+', '', cleaned)  # Removes mentions
	cleaned = re.sub(r'((www\.[^\s]+)|(https?://[^\s]+))','',cleaned) # Removes hyperlink	
	cleaned = re.sub(r'[\s]+', ' ', cleaned)  # Removes additional white spaces
	cleaned = cleaned.strip('\'"').lstrip().rstrip() # Trim
	return cleaned


import re
import csv
data = open('output/KEYWORD_SEARCH_OUTPUT.csv','r')
reader = csv.DictReader(data)
with open('output.csv','w') as file:
	fieldnames = [
		'user',
		'search query', 
		'post date-time', 
		'account status', 
		'account sentiment',
		'account sentiment score', 
		'retweet status', 
		'retweet sentiment',
		'retweet sentiment score',
		'post location', 
		'tweet id',
		'account subjectivity', 
		'account subjectivity score',
		'retweet subjectivity', 
		'retweet subjectivity score',
		'tones'
	]
	writer = csv.DictWriter(file, fieldnames=fieldnames)
	writer.writeheader()
	for row in reader:
		row['account status'] = cleanData(row['account status'])
		text = row.get('account status',None)
		g = str(text).encode()
		import pdb; pdb.set_trace()	
		tones = tone_analyzer.tone(tone_input=text,content_type='text/plain;charset=utf-8')
		print(tones.get_result())
		writer.writerow(row)

data.close()

# df['account status'] = df['account status'].apply(cleanData)

# for index, row in df.iterrows():
# 		text = row['account status']
# 		tones = tone_analyzer.tone(text,content_type='text/plain;charset=utf-8')
# 		print(tones.get_result())

# 	#df['new'] = df['account status'] + 'Wassup!'

# #findTones('Can the COVID-19 Pandemic affect the production of autonomous vehicles?')


# df.to_csv('test.csv')


'''
JSON OUTPUT
{'document_tone': 
	{'tones': 
		[
			{'score': 0.659214, 'tone_id': 'anger', 'tone_name': 'Anger'}, 
			{'score': 0.869578, 'tone_id': 'confident', 'tone_name': 'Confident'}
		]
	}, 
'sentences_tone': 
[
	{
		'sentence_id': 0, 'text': 'I hate the new Tesla Model X.', 
		'tones': [{'score': 0.758945, 'tone_id': 'anger', 'tone_name': 'Anger'}]
	}, 
	{'sentence_id': 1, 'text': 'It is the worst car I have ever seen', 
		'tones': [{'score': 0.660207, 'tone_id': 'confident', 'tone_name': 'Confident'}]
	}
]
}
Really only want document_tone (per tweet and also entire document)
use get to obtain document tones
strength if > .75 (can do a mask or something here to make this easy)
and then columns for everything
Emotional Tones: anger, disgust, fear, joy, sadness
Writing Tones: analytical, confident, tentative
'''