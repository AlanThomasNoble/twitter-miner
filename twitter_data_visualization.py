import sys
import os
import matplotlib.pyplot
import datetime
import itertools
import collections
import pandas
from nltk.corpus import stopwords
from twitter_nlp import cleanTxt #removes URL, username, and whitespace / gets rid of hashtag / makes lowercase

from datavis import Visuals
from twitter_miner_1 import exit_program

stopwords_set = set(stopwords.words('english'))

# The UI provided to the user
def start():
    print()
    print("This software will be used to output data visualizations.")
    print()
    print("(1) Pos - returns word freq graph for positive sentiment tweets")
    print("(2) Neg - returns word freq graph for negative sentiment tweets")
    print("(3) Date - returns word freq graph for a date range")
    print("(4) Pie - returns pie chart: Positive, Neutral, and Negative Tweets")
    print("(4) wordCloud")
    print("(5) ngrams")
    print("(6) polSub")
    print("(7) valueCount")
    print()
    data = input("Enter the type of data visualization you would like (Ex: Pos, Neg, etc...): ")
    print()
    print("Available Files [Please Do Not Include Extension in Entry (.csv)]: ")
    os.system('cd output && ls *.csv') # or *.db
    fileName = input("Choose FileName to Perform Visualization (i.e. tweets): ")
    print()
    return data, fileName


# returns list of clean/preprocessed tweets based on the sentiment that you are trying to analyse
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


# returns list of clean/preprocessed tweets based on the date range that you provide
# [5-17-1999, 5-17-2020] -> includes both start and end date
# just based off account status as of now -> maybe add retweet status later
def get_list_based_on_dates(file):
    print("Enter the following dates in this format: M-D-YYYY Ex: 5-17-1999, 12-2-2019)")
    start_date = input("Enter the start date: ")
    end_date = input("Enter the end date: ")
    
    start_list = start_date.split('-')
    start_day = int(start_list[1])
    start_month = int(start_list[0])
    start_year = int(start_list[2])
    start_datetime = datetime.datetime(
        start_year, 
        start_month, 
        start_day, 
        0, 
        0, 
        0
    )

    end_list = end_date.split('-')
    end_day = int(end_list[1])
    end_month = int(end_list[0])
    end_year = int(end_list[2])
    end_datetime = datetime.datetime(
        end_year, 
        end_month, 
        end_day, 
        0, 
        0, 
        0
    )

    print(start_datetime, end_datetime)

    col_list = ["post date-time", "account status"]
    df = pandas.read_csv(f"output/{file}", usecols=col_list)

    processed_tweets = []
    for ind in df.index: 
        print(1, start_datetime)
        print(1, df["post date-time"][ind])
        datetime_list = df["post date-time"][ind].split(' ')
        date_list = datetime_list[0].split('-')
        time_list = datetime_list[1].split(':')
        cur_datetime = datetime.datetime(
            int(date_list[0]), 
            int(date_list[1]), 
            int(date_list[2]), 
            int(time_list[0]), 
            int(time_list[1]), 
            int(time_list[2])
        )
        print(2, cur_datetime)

        print("result", cur_datetime > start_datetime)
        if (cur_datetime >= start_datetime and cur_datetime <= end_datetime) and isinstance(df["account status"][ind], str):
            text = cleanTxt(df["account status"][ind])
            processed_tweets.append(text)

    return processed_tweets


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

    return counter_list.most_common(int(num))


# returns word frequency graph
def show_freq_graph(dic, description):
    df_from_dic = pandas.DataFrame(dic, columns=["words", "count"])

    fig, ax = matplotlib.pyplot.subplots(figsize=(8,8))

    # creates the horizontal bar graph
    df_from_dic.sort_values(by="count").plot.barh(
        x='words', 
        y='count',
        ax=ax,
        color='green'
    )

    # prints the graph
    ax.set_title(f"Common Words Found in Tweets ({description})")
    matplotlib.pyplot.show()


# Outputs a pie chart comparing the number of positive, neutral, and negative tweets in a CSV
# Helps us gauge positive and negative distributions amongst the tweets
# INCLUDES BOTH ACCOUNT AND RETWEET STATUSES
def pos_vs_neg_pie(file):
    col_list = ["account sentiment", "retweet sentiment"]
    df = pandas.read_csv(f"output/{file}", usecols=col_list)
    
    num_pos = 0
    num_neg = 0
    num_neut = 0

    for ind in df.index: 
        if df["account sentiment"][ind] and df["account sentiment"][ind] == "positive":
            num_pos += 1
        if df["account sentiment"][ind] and df["account sentiment"][ind] == "negative":
            num_neg += 1
        if df["account sentiment"][ind] and df["account sentiment"][ind] == "neutral":
            num_neut += 1

        if df["retweet sentiment"][ind] and df["account sentiment"][ind] == "positive":
            num_pos += 1
        if df["retweet sentiment"][ind] and df["account sentiment"][ind] == "negative":
            num_neg += 1
        if df["retweet sentiment"][ind] and df["account sentiment"][ind] == "neutral":
            num_neut += 1
        
    # Data to plot
    labels = 'Positive', 'Neutral', 'Negative'
    sizes = [num_pos, num_neut, num_neg]
    colors = ['yellowgreen', 'gold', 'lightcoral']
    # explode = (0.1, 0, 0, 0)  # explode 1st slice

    # Plot
    matplotlib.pyplot.pie(sizes, labels=labels, colors=colors,
    autopct='%1.1f%%', shadow=True, startangle=140)

    matplotlib.pyplot.axis('equal')
    matplotlib.pyplot.show()


def main():
    user_input = start()
    if user_input[0] == "Pos":
        processed_tweets = get_list_based_on_sentiment("positive", user_input[1] + ".csv")
        dic = word_freq_generator(processed_tweets)
        show_freq_graph(dic, "Positive Sentiment")

    elif user_input[0] == "Neg":
        processed_tweets = get_list_based_on_sentiment("negative", user_input[1] + ".csv")
        dic = word_freq_generator(processed_tweets)
        show_freq_graph(dic, "Negative Sentiment")

    elif user_input[0] == "Date":
        processed_tweets = get_list_based_on_dates(user_input[1] + ".csv")
        dic = word_freq_generator(processed_tweets)
        show_freq_graph(dic, "Date Range")
    
    elif user_input[0] == "Pie":
        pos_vs_neg_pie(user_input[1] + ".csv")

    elif user_input[0] == "wordCloud":
        try:
            v = Visuals(user_input[1], "wordCloud")
        except ValueError:
            exit_program()

    elif user_input[0] == "ngrams":
        try:
            v = Visuals(user_input[1], "ngrams")
        except ValueError:
            exit_program()

    elif user_input[0] == "polSub":
        try:
            v = Visuals(user_input[1], "polSub")
        except ValueError:
            exit_program()

    elif user_input[0] == "valueCount":
        try:
            v = Visuals(user_input[1], "valueCount")
        except ValueError:
            exit_program()

    else:
        print("Program exited.")
        sys.exit()

    return 0


if __name__ == "__main__":
    main()
