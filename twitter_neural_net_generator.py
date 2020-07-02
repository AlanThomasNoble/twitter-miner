# File for building a neural network using TensorFlow and Keras, and then using this neural network to classify tweets

# 1) Get our data into a usable format
# 2) Build our neural net
# 3) Train it with said data
# 4) Save the neural net for future use

#################################################### PREPROCESSING ############################################################
import re

# Alternative/Merged Implementation of Clean Text
'''This implementation entirely removes hashtags and mentions'''
'''pythex.org'''
def cleanTextNN(text, cleanEmoticons=False):
    # Conversions
    text = text.lower() # Convert to lowercase
    
    # Removals
    text = re.sub(r'@[A-Za-z0-9]+','',text) # Removes mentions
    text = re.sub(r'#[A-Za-z0-9_]+','',text) # Removes hashtags
    text = re.sub(r'(https?)://[-a-zA-Z0-9@:%_\+.~#?&//=]*','',text) # Removes hyperlink

    # Cleanup
    text = re.sub('[\s]+',' ',text) # Removes additional white spaces
    text = text.strip('\'"').lstrip().rstrip() # Trim (Removes '' and Trailing and Leading Spaces)

    if cleanEmoticons:
        pass    # :\)|:-\)|:\(|:-\(|;\);-\)|:-O|8-|:P|:D|:\||:S|:\$|:@|8o\||\+o\(|\(H\)|\(C\)|\(\?\)

    return text


###############################################################################################################################

############################################# GETTING DATA IN USABLE FORMAT ###################################################

import numpy as np
print("1")
# extract columns 1 and 3 from the CSV
training = np.genfromtxt('/Users/alannoble/Documents/Autonomous-Vehicles-Research/Neural-Net-Files/Sentiment_Analysis_Dataset.csv', 
    delimiter=',',
    skip_header=1,
    usecols=(1, 3), 
    dtype=None
)

# list of all the tweets
train_x_before = [x[1] for x in training]
train_x = [cleanTextNN(tweet) for tweet in train_x_before]
# print(len(train_x_before))
# print(train_x_before[1])
# print(len(train_x))
# print(train_x[1])
# sys.exit()

# list of all the respective sentiment labels
train_y = np.asarray([x[0] for x in training])

import json
import keras
import keras.preprocessing.text as kpt
from keras.preprocessing.text import Tokenizer

# only work with the 3000 more popular words from out dataset
max_words = 3000

# create a new tokenizer
tokenizer = Tokenizer(num_words = max_words) # turns each text into a sequence of integers in order to apply machine learning

# feed our tweets to the tokenizer
tokenizer.fit_on_texts(train_x) # This method creates the vocabulary dict based on word frequency: cat->1 dog->2

dictionary = tokenizer.word_index # Dictionary of word to ID/index

# moves the dictionary that we just got to a file called nn_dictionary.json in the output folder
with open('/Users/alannoble/Documents/Autonomous-Vehicles-Research/Neural-Net-Files//nn_dictionary.json', 'w') as dictionary_file:
    json.dump(dictionary, dictionary_file)

def convert_text_to_index_array(text):
    # text to word sequence converts text to a list of words. A cat and the hat -> [A, cat, and, the, hat]
    # returns list with ids/index for all the words
    return [dictionary[word] for word in kpt.text_to_word_sequence(text)]

# for each tweet, take the text, and convert the text to a list of its ID/Index then add that list to a master list
allWordIndices = []
for text in train_x:
    indices_for_each_word_in_text_list = convert_text_to_index_array(text)
    allWordIndices.append(indices_for_each_word_in_text_list)

# cast as an array for future use??
allWordIndices = np.asarray(allWordIndices)

train_x = tokenizer.sequences_to_matrix(allWordIndices, mode='binary')
train_y = keras.utils.to_categorical(train_y, 2) #update


##############################################################################################################################

############################################# BUILDING OUT NEURAL NETWORK ####################################################

from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
print("2")
# Building the neural net
# relu is an activation function - all the activatioin functions in keras/tensorflow are viable
model = Sequential() # a simple type of neural network that consists of a stack of layers executed in that order
model.add(Dense(512, input_shape=(max_words,), activation='relu')) # 512 nodes
model.add(Dropout(0.5)) # used to randomly remove data to prevent overfitting
model.add(Dense(256, activation='sigmoid'))
model.add(Dropout(0.5))
model.add(Dense(2, activation="softmax")) # might need to change to 3 later because 3 possible classifications update

# now we need to compile this neural network
model.compile(loss='categorical_crossentropy', optimizer="adam", metrics=['accuracy'])
# the accuracy metric will give us helpful output on how well our NN is performing


##############################################################################################################################

############################################# TRAINING THE NEURAL NETWORK ####################################################
print("3")
# 5 epochs is said to be good, experimenting is possible, don't want overfitting
# validation split - identifying how much of your input should be used for testing. 10 percent
model.fit(train_x, train_y, 
    batch_size=32, 
    epochs=5, 
    verbose=1, 
    validation_split=0.1, 
    shuffle=True
)

##############################################################################################################################

############################################### SAVING THE NEURAL NETWORK ####################################################
print("4")
model_json = model.to_json()
with open('/Users/alannoble/Documents/Autonomous-Vehicles-Research/Neural-Net-Files//model.json', 'w') as json_file_w_NN:
    json_file_w_NN.write(model_json)
model.save_weights('/Users/alannoble/Documents/Autonomous-Vehicles-Research/Neural-Net-Files//model.h5')
