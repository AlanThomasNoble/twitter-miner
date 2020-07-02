import numpy as np 
from wordcloud import WordCloud
import matlablib.pyplot as plt

# import pandas as pd # dataframe

# streamline main()

# dict(mood=mood, polarity=polarity,subjectivity=subjectivity)
    # g.update(f) to connect to dicts together, pass into DataFrame.

# Write this as a Class
def wordCloud(data, spec=''):
	pass

def ngram(data, spec=''):
	pass

def vis(filename, visualization, spec):
	# Read in Data to a DataFrame
	with open(filename,'r') as file:
		pass # read in data here
		data = []
	
	return visualization(data, spec)