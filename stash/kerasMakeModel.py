# Blog: https://vgpena.github.io/classifying-tweets-with-keras-and-tensorflow/
# Source Code: https://gist.github.com/vgpena/b1c088f3c8b8c2c65dd8edbe0eae7023
# Twitter DataSet: http://thinknook.com/twitter-sentiment-analysis-training-corpus-dataset-2012-09-22/

# Custom neural net that can classify text as positive or negative with 79.3% accuracy.

'''
Neural nets can take anywhere from a few moments to days to train, 
depending on your hardware and on how large and/or complex your dataset is. 
This net took me ~60 minutes to train on a mid-2015 MacBook Pro (and it got NOISY 😅 ). 
My point is, you probably won’t want to have to train the net every single time you want to use it. 
he last step of our training script will also save the net so that we can “boot it up” 
quickly from another script when we actually want to consult it.
'''

# Steps
# > Get data into a usable format
# > Build neural net
# > Train it with data
# > Save the neural net for future use

import json
import keras
import keras.preprocessing.text as kpt
from keras.preprocessing.text import Tokenizer

import numpy as np
# Extract CSV Data (Columns 1 and 3, Skip First Line (Header))
training = np.genfromtxt('/path/to/your/data.csv', delimiter=',', skip_header=1, usecols=(1, 3), dtype=None)

# Create Training Data
train_x = [str(x[1]) for x in training] # python3 fix
# train_x = [x[1] for x in training]

# Index Sentiment Labels with Numpy
train_y = np.asarray([x[0] for x in training])

# Only works with max 3000 words used in our datset.
max_words = 3000

# Create New Tokenizer
tokenizer = Tokenizer(num_words=max_words)

# Feed Tweets to Tokenizer
tokenizer.fit_on_texts(train_x)

# Tokenizers come with a convenient list of words and IDs
dictionary = tokenizer.word_index
# Save List of Words (json format)
with open('dictionary.json', 'w') as dictionary_file:
    json.dump(dictionary, dictionary_file)

def convert_text_to_index_array(text):
    return [dictionary[word] for word in kpt.text_to_word_sequence(text)] 
    # makes all texts the same length -- in this case, the length
    # of the longest text in the set.

allWordIndices = []
# for each tweet, change each token to its ID in the Tokenizer's word_index
for text in train_x:
    wordIndices = convert_text_to_index_array(text)
    allWordIndices.append(wordIndices)

# Now, we have list of all tweets converted to index arrays.
# Cast as array for future
allWordIndices = np.asarray(allWordIndices)

# Create one-hot matrices out of the indexed tweets
train_x = tokenizer.sequences_to_matrix(allWordIndices, mode='binary')
# Treat Labels at categories
train_y = keras.utils.to_categorical(train_y, 2)

from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation

model = Sequential()
model.add(Dense(512, input_shape=(max_words,), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(256, activation='sigmoid'))
model.add(Dropout(0.5))
model.add(Dense(2, activation='softmax'))

model.compile(loss='categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy'])

model.fit(train_x, train_y,
    batch_size=32,
    epochs=5,
    verbose=1,
    validation_split=0.1,
    shuffle=True)

model_json = model.to_json()
with open('model.json', 'w') as json_file:
    json_file.write(model_json)

model.save_weights('model.h5')

print('saved model!')
