#import os
#os.environ["CORENLP_HOME"] = '/Users/Sangeetha/Desktop/Research/stanford-corenlp-4.0.0'

# Import client module
from stanza.server import CoreNLPClient
import pdb

text = "Chris Manning is a nice person. Chris wrote a simple sentence. He also gives oranges to people."
with CoreNLPClient(
		annotators=['tokenize','ssplit','pos','lemma','ner', 'parse', 'depparse','coref','sentiment'],
		be_quiet=False,
        timeout=30000,
        memory='16G') as client: # context manager
	ann = client.annotate(text)
print(ann)
pdb.set_trace()
for s in results["sentences"]:
    print("{} : {}".format(" ".join(t["word"] for t in s["tokens"]),s["sentiment"]))


'''
client = CoreNLPClient(timeout=150000000, be_quiet=False, annotators=['tokenize','ssplit', 'pos', 'lemma', 'ner'], memory='16G', endpoint='http://localhost:9000')
print(client)

#client.start()
#import time; time.sleep(10)

text = "Albert Einstein was a German-born theoretical physicist. He developed the theory of relativity."
print (text)
document = client.annotate(text)
print ('malviya')
print(type(document))
'''

'''
from stanza.server import CoreNLPClient
import pdb
text = "Chris Manning is a nice person. Chris wrote a simple sentence. He also gives oranges to people."
with CoreNLPClient(
        annotators=['tokenize','ssplit','pos','lemma','ner', 'parse', 'depparse','coref'],
        timeout=30000,
        memory='16G') as client:
    results = client.annotate(text)

pdb.set_trace()
for s in results["sentences"]:
    print("{} : {}".format(" ".join(t["word"] for t in s["tokens"]),s["sentiment"]))

'''
'''
To start Program:
export CORENLP_HOME=/Users/Sangeetha/Desktop/Research/stanford-corenlp-4.0.0
export CLASSPATH=stanford-corenlp-3.9.1.jar:stanford-corenlp-3.9.1-models.jar
'''

'''
with CoreNLPClient(properties={
      'annotators': 'tokenize,ssplit,pos',
      'pos.model': '/path/to/custom-model.ser.gz'
  }) as client:
'''


# import stanza # new version of Stanford CoreNLP
# # Building a Pipeline
# stanza.download('en') # Downloads English models for neural pipeline.
# nlp = stanza.Pipeline('en') # Sets up default neural pipeline in English

# # Analysis
# doc = nlp("Barack Obama was born in Hawaii.  He was elected president in 2008.")

# # view
# doc.sentences[0].print_dependencies() # Prints words in first sentence or input string (or Document, as it is represented by Stanza)
# print(doc)
# print(doc.entities)

# '''
# Within a Document, annotations are further stored in Sentences, Tokens, Words in a top-down 
# fashion. An additional Span object may be used to store annotations such as named entity mentions. 
# Here we provide some simple examples to manipulate the returned annotations.
#   >The following example shows how to print the text, lemma and POS tag of each word in each 
#   sentence of an annotated document:
# '''
# for sentence in doc.sentences:
#     for word in sentence.words:
#         print(word.text, word.lemma, word.pos)
# # The following example shows how to print all named entities and dependencies in a document:

# for sentence in doc.sentences:
#     print(sentence.ents)
#     print(sentence.dependencies)
   