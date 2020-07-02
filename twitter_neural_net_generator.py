
# 1) Get our data into a usable format
# 2) Build our neural net
# 3) Train it with said data
# 4) Save the neural net for future use

import numpy as np

# extract columns 1 and 3 from the CSV
training = np.genfromtxt('/Users/alannoble/Documents/Autonomous-Vehicles-Research/Sentiment_Analysis_Dataset.csv', delimiter=',', skip_header=1, usecols=(1, 3), dtype=None)
print(len(training))


# create our training data from the tweets
train_x = [x[1] for x in training]
# index all the sentiment labels
train_y = np.asarray([x[0] for x in training])