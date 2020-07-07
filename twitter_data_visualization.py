import sys
import datetime
import itertools
import collections
import pandas
from nltk.corpus import stopwords
from twitter_nlp import cleanTxt #removes URL, username, and whitespace / gets rid of hashtag / makes lowercase

stopwords_set = set(stopwords.words('english'))

def start():
    print()
    print("This software will be used to output data visualizations.")
    print()
    print("(1) Pos - returns word freq graph for positive sentiment tweets")
    print("(2) Neg - returns word freq graph for negative sentiment tweets")
    print("(2) Date - returns word freq graph for a date range")
    print()
    data = input("Enter the type of data visualization you would like (Ex: Pos, Neg, Date.): ")
    print()
    file_name = input("Enter the name of the file in the output folder would you like to visualize: ")
    print()
    return [data, file_name]


# returns list of tweets based on the sentiment that you are trying to analyse
# sentiment = positive -> returns list of positive tweets
# sentiment = negative -> returns list of negative tweets
# just based off account status as of now -> maybe add retweet status later
def get_list_based_on_sentiment(sentiment, file):
    col_list = ["account status", "account sentiment"]
    df = pandas.read_csv(f"output/{file}", usecols=col_list)

    processed_tweets = []
    for ind in df.index: 
        if isinstance(df["account status"][ind], str) and df["account sentiment"][ind] == sentiment:
            text = cleanTxt(df["account status"][ind])
            processed_tweets.append(text)

    return processed_tweets


def get_list_based_on_dates(file):
    print("Enter the following dates in this format: M-D-YYYY")
    start_date = input("Enter the start date (Ex: 5-17-1999): ")
    end_date = input("Enter the end date (5-17-2020): ")
    
    start_list = start_date.split('-')
    start_day = int(start_list[0])
    start_month = int(start_list[1])
    start_year = int(start_list[2])
    start_datetime = datetime.datetime(start_year, start_month, start_day, 0, 0, 0)

    end_list = end_date.split('-')
    end_day = int(end_list[0])
    end_month = int(end_list[1])
    end_year = int(end_list[2])
    end_datetime = datetime.datetime(end_year, end_month, end_day, 0, 0, 0)

    print(start_datetime, end_datetime)

    was_date1_before = start_datetime < end_datetime

    print(was_date1_before)

# prints a word frequency dictionary
def word_freq_generator(processed_tweets):
    num = input("Enter the number of results you would like in your frequency graph: ")

    # create list for each tweet
    words_list_for_each_tweet = [tweet_text.split() for tweet_text in processed_tweets]
    
    # Remove stop words from each tweet list of words
    tweets_without_stopwords = [[word for word in tweet_words if not word in stopwords_set] for tweet_words in words_list_for_each_tweet]
    words_list_final = list(itertools.chain(*tweets_without_stopwords)) # flattens the list so that all the words are in one list

    # calculate frequencies
    counter_list = collections.Counter(words_list_final)

    print(counter_list.most_common(int(num)))
    # print data graph


def main():
    user_input = start()
    if user_input[0] == "Pos":
        processed_tweets = get_list_based_on_sentiment("positive", user_input[1])
        word_freq_generator(processed_tweets)
    elif user_input[0] == "Neg":
        processed_tweets = get_list_based_on_sentiment("negative", user_input[1])
        word_freq_generator(processed_tweets)
    elif user_input[0] == "Date":
        get_list_based_on_dates(user_input[1])
    else:
        print("Program exited.")
        sys.exit()

    return 0

if __name__ == "__main__":
    main()
