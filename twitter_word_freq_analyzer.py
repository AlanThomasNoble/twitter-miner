# Requirements: CSV dataset, start and end dates
# Output: Graph of the most common words / choose any number
import itertools
import collections
import pandas
from twitter_nlp import cleanTxt #removes URL, username, and whitespace / gets rid of hashtag / makes lowercase

def get_CSV_based_on_sentiment(sentiment):
    pass

def get_CSV_based_on_dates(date_start, date_end):
    pass

def word_freq_generator():
    how_many = 10
    col_list = ["account status"]
    df = pandas.read_csv("output/FULL_TEXT_LIST.csv", usecols=col_list)

    processed_tweets = []
    for ind in df.index: 
        if isinstance(df["account status"][ind], str):
            processed_tweets.append(cleanTxt(df["account status"][ind]))


    words_list_for_each_tweet = [tweet_text.split() for tweet_text in processed_tweets]
    words_list_final = list(itertools.chain(*words_list_for_each_tweet)) # flattens the list so that all the words are in one list

    counter_list = collections.Counter(words_list_final)
    print(counter_list.most_common(how_many))
    # print data graph

def main():
    word_freq_generator()
    return 0

if __name__ == "__main__":
    main()
