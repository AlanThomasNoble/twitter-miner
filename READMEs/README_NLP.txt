LIBRARY #1: nltk/textblob
    https://www.pluralsight.com/guides/natural-language-processing-extracting-sentiment-from-text-data
    https://medium.com/better-programming/twitter-sentiment-analysis-15d8892c0082 

    SETTING UP THE PYTHON ENVIRONMENT AND THE NECESSARY LIBRARIES
        python3.6 -m venv env
        source env/bin/activate
        which python
        which python3.6
        pip install -U nltk
        pip install -U textblob
        python3.6 -m textblob.download_corpora
        /Users/alannoble/Documents/Autonomous-Vehicles-Research/Twitter-NLP/env/bin/python3.6 /Users/alannoble/Documents/Autonomous-Vehicles-Research/Twitter-NLP/twitter_NLP.py

        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context
        nltk.download()

    Output: 
        Sentiment(polarity=0.7000000000000001, subjectivity=0.825)
        
        Polarity 
        -> float type
        -> [-1, 1]
        -> 1 indicates a highly positive sentiment
        -> -1 indicates a highly negative sentiment

        Subjectivity
        -> float type
        -> [0, 1]
        -> 1 mostly public opinion/not a factual piece of information
        -> 0 factual

LIBRARY #2
Building a neural network using TensorFlow and Keras

    source env/bin/activate
    pip install numpy
    pip install keras
    pip install tensorflow
    

