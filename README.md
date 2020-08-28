# General Overview
To start program, type __make__

> Note: Check Python dependencies in twitter_miner, twitter_main, twitter_nlp, twitter_processing, twitter_datavis are all installed.

You'll then be presented with two options: _mine_ or _visuals_.

__mine:__ this selection will direct you to a place to help you mine tweets.

__visuals:__ this selection will direct you to a place to generate visualizations based on mined data.

All terminal UI is contained in twitter_main.py for clarity.

# Twitter Miner
This program helps you compile large Twitter datasets. It is written in Python 3.6.

Requirements: Python 3.6

1) Activate the Python environment
source env/bin/activate

2) The following is the terminal command to run the program
/...Current Working Directory.../env/bin/python3.6 /...Current Working Directory.../twitter_main.py

3) Follow the directions stated in the std. output in the terminal. It will walk you through the steps of running the program.

4) There are a multiple features that are available as of now: obtaining tweets from a single user, 
obtaining tweets from a list of users, and performing search queries


# Twitter Watson
File: __twitter_watson.py__

This file generates emotional scores with IBM Watson.  After generating a file with Twitter Miner above, change the `file` variable in the script to the name of the generated file from Twitter Miner.  Remember to edit the input and output location in the _read_csv()_, _to_csv()_ lines as well.

Then, run program: `python3 twitter_watson.py`


> Note: To run this program, an IBM Watson free account is required.  Set up your own account here: link.  Then, set up a natural language understanding service.  Paste the _api key_ and _url_ from the service into the script in the "Authentication" section.


# Twitter Datavis and Twitter Processing
File: __twitter_datavis.py__, __twitter_procsesing.py__

The datavis file provides the backend for the _visuals_ selection.
The processing file stores some of the filtering/cleaning functions of the datavis script.

The datavis file contains a class which holds all the visualization functions.  The `__init__` function initializes parameters, sorts the entries by date, cleans the data (function is in processing), and then calls all the requested visualizations in a loop.  `editDataframe()` is called within `__init__` to allow the user to constrain the given data by sentiment, subjectivity, and date range.

Current Visualization Options: Bar, Stacked Bar, Barh, Pie, Radar Chart, Time Series, Word Cloud, Bar Chart Race, among more.

It's easy to create a new visualization.  Create a new function within the class. Use `self.df` and a Python library (i.e. matplotlib, Plotly) to generate a desired visualizations. Remember to update the `__init__` function and _twitter_main.py_ whenever a new function is added.