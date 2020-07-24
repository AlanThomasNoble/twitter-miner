# External Libraries
import re

# Internal Libraries
import stopwords # sourced from spacy


#####################################################################################################
'''Processing Functions'''
##################################################################################################### 

def cleanData(text, correctSpelling=False):
	'''Removes Emojis, Mentions, Hashtags, and https Hyperlinks

	Notes: 
		> strings are not being passed in implicitly, requiring convert.
		> clean all columns for NaN, nan and '' values.
		
	Parameters
	----------
	text : str
		Input string to be cleaned

	Returns
	-------
	str
		String of cleaned input text
	'''

	# Lower text (Simplifies processing)
	text = str(text).lower()

	# Removals
	text = re.sub(r'@[A-Za-z0-9]+', '', text)  # Removes mentions
	text = re.sub(r'#([^\s]+)', r'\1', text) #Replace #word with word
	text = re.sub(r'((www\.[^\s]+)|(https?://[^\s]+))','',text) # Removes hyperlink
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
	
	# Cleanup
	text = re.sub(r'[\s]+', ' ', text)  # Removes additional white spaces
	text = text.strip('\'"').lstrip().rstrip() # Trim
	
	# Spelling Correction (https://textblob.readthedocs.io/en/dev/quickstart.html#spelling-correction)
	# Taking a really long time... to finish.
	if correctSpelling:
		from textblob import TextBlob
		text = str(TextBlob(text).correct()) 

	return text


def tokenizeText(tweets):
	'''Tokenizes text from dataframe input

	Notes: 
		> '','nan' being added weirdly.
		> Debating whether to replace contractions (i.e. isn't -> is not)
		> Edge Case: 'this--however' (em dashes) (Morgan-Stanley) [Potential Solution: Remove all Dashes]
		> NLTK impl: nltk.download('punkt'); tokens = nltk.word_tokenize(tweets) (not sure if this impl is desired)

	Parameters
	----------
	tweets : ? (some pandas type.)
		Column selection of tweets to be tokenized.

	Returns
	-------
	list
		A list of words (tokens) based on input text.
	'''

	# Split
	weird = ['', 'nan']  # '' not working, nan working
	tokens = ' '.join(t for t in tweets if t not in weird)
	tokens = tokens.split(' ')

	# Remove non-alphanumeric characters at the end or beginning of a word.
	tokens = [re.sub(r"^\W+|\W+$", "", word) for word in tokens]

	# Return
	return tokens


def removeStopwords(tokens):
	'''Removes common words (stopwords) and simple web links.

	Notes:

	Parameters
	----------
	tokens : str
		The sound the animal makes (default is None)

	Returns
	-------
	list
		A list of words with stopwords removed.
	'''

	domains = ('.com', '.org', '.gov', '.ny', '.edu')
	return [t for t in tokens if t not in (stopwords.STOP_WORDS or stopwords.AV_STOP_WORDS) and not t.endswith(domains)]


def expandAbbr(tokens):
	'''Expands common twitter abbreviations to full text.

	Notes:
		> Make function similar to removeStopwords()
		> Create a file of abbreviations, abbrs.py
		> import abbrs

	Parameters
	----------
	tokens : str
		A list of words (str)

	Returns
	-------
	list
		A list of words with abbreviations expanded.
	'''


def lemmatizeText(tokens):
	'''Removes common words (stopwords) and simple web links.
	Converts input list of strings to list of spacy token objects in order to lemmatize,
	then converts them back to strings and appends them to output list.
	NOTE: User must have spacy en library downloaded.
	Run: python3 -m spacy download en_core_web_sm
	
	Parameters
	----------
	tokens : list
		A list of words (str)

	Returns
	-------
	list
		A list of words (str) with each word lemmatized, if applicable.
	'''
	
	out = "".join(tokens)
	nlp = spacy.load('en')
	doc = nlp(out)
	output = []
	for token in doc:
    	output.append(token.lemma_)
	return output