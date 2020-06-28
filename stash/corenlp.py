from pycorenlp import StanfordCoreNLP

nlp = StanfordCoreNLP('http://localhost:9000')
res = nlp.annotate("I love you. I hate him. You are nice. He is dumb",
                   properties={
                       'annotators': 'sentiment',
                       'outputFormat': 'json',
                       'timeout': 1000,
                   })
for s in res["sentences"]:
    print("%d: '%s': %s %s" % (
        s["index"],
        " ".join([t["word"] for t in s["tokens"]]),
        s["sentimentValue"], s["sentiment"]))

# '''
# from pycorenlp import StanfordCoreNLP
# nlp = StanfordCoreNLP('http://localhost:9000')
# text = "The intent behind the movie was great, but it could have been better"
# results = nlp.annotate(text,properties={
#         'annotators':'sentiment, ner, pos',
#         'outputFormat': 'json',
#         'timeout': 50000,
#         })
# for s in results["sentences"]:
#     print("{} : {}".format(" ".join(t["word"] for t in s["tokens"]),s["sentiment"]))




# #  java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer
# '''

# import os
# os.environ["CORENLP_HOME"] = '/Users/Sangeetha/Desktop/Research/stanford-corenlp-4.0.0'

# # Import client module
# from stanza.server import CoreNLPClient


# client = CoreNLPClient(timeout=150000000, be_quiet=False, annotators=['sentiment','ner','pos'], memory='16G', endpoint='http://localhost:9000',outputFormat='json')
# print(client)

# #client.start()
# #import time; time.sleep(10)

# text = "This movie was actually neither that funny, nor super witty. The movie was meh. I liked watching that movie. If I had a choice, I would not watch that movie again."
# print (text)
# document = client.annotate(text)
# print ('malviya')
# print(type(document))
# ''''
# for d in document["sentences"]:
#     print("{} : {}".format(" ".join(t["word"] for t in s["tokens"]),s["sentiment"]))
#     '''

# print("{}: '{}': {} (Sentiment Value) {} (Sentiment)".format(
#         d["index"],
#         " ".join([t["word"] for t in d["tokens"]]),
#         d["sentimentValue"], d["sentiment"]))
 
