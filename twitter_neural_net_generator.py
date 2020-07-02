# File for building a neural network using TensorFlow and Keras, and then using this neural network to classify tweets

# 1) Get our data into a usable format
# 2) Build our neural net
# 3) Train it with said data
# 4) Save the neural net for future use

############################################# GETTING DATA IN USABLE FORMAT ###################################################

import numpy as np

# extract columns 1 and 3 from the CSV
training = np.genfromtxt('/Users/alannoble/Documents/Autonomous-Vehicles-Research/Sentiment_Analysis_Dataset.csv', delimiter=',', skip_header=1, usecols=(1, 3), dtype=None)
# print(len(training)) -> 1578627

# list of all the tweets
train_x = [x[1] for x in training]

# list of all the respective sentiment labels
train_y = np.asarray([x[0] for x in training])

import sys
import json
import keras
import keras.preprocessing.text as kpt
from keras.preprocessing.text import Tokenizer

# only work with the 3000 more popular words from out dataset
max_words = 3000

# create a new tokenizer
tokenizer = Tokenizer(num_words = max_words) # turns each text into a sequence of integers in order to apply machine learning

# feed our tweets to the tokenizer
tokenizer.fit_on_text(train_x) # This method creates the vocabulary dict based on word frequency: cat->1 dog->2

dictionary = tokenizer.word_index # Dictionary of word to ID/index

# moves the dictionary that we just got to a file called nn_dictionary.json in the output folder
with open(output/nn_dictionary.json, 'w') as dictionary_file:
    json.dump(dictionary, dictionary_file)

def convert_text_to_index_array(text):
    # text to word sequence converts text to a list of words. A cat and the hat -> [A, cat, and, the, hat]
    # returns list with ids/index for all the words
    return [dictionary[word] for word in kpt.text_to_word_sequence(text)]

# for each tweet, take the text, and convert the text to a list of its ID/Index then add that list to a master list
allWordIndices = []
for text in train[x]:
    indices_for_each_word_in_text_list = convert_text_to_index_array(text)
    allWordIndices.append(indices_for_each_word_in_text_list)

# cast as an array for future use??
allWordIndices = np.asarray(allWordIndices)

train_x = tokenizer.sequences_to_matrix(allWordIndices, mode='binary')
train_y = keras.utils.to_categorical(train_y, 2)


##############################################################################################################################

############################################# BUILDING OUT NEURAL NETWORK $###################################################








