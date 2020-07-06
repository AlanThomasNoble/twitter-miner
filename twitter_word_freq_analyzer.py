# Requirements: CSV dataset, start and end dates
# Output: Graph of the most common words / choose any number

from twitter_nlp import cleanTxt #removes URL, username, and whitespace / gets rid of hashtag / makes lowercase

def common_words_generator():

    all_tweets = []
    processed_tweets = [cleanTxt(tweet) for tweet in all_tweets]

    # remove stop words

    words_list_for_each_tweet = [tweet_text.split() for tweet_text in processed_tweets]
    words_list_final = list(itertools.chain(*words_list_for_each_tweet))

    counter_list = collections.Counter(words_list_final)
    counter_list.most_common(3)

    print(counter_list)
    # print data graph

def main():


if __name__ == "__main__":
    main()
