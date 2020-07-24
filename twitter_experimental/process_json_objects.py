import json
import csv
import tweepy
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
import twitter_nlp
import time

consumer_key = "e9phIIirNUPdAX8IvMFqQSzDp"
consumer_secret = "4Mnv0GBAWly06Wcf3U4Gzo98tvWqrpdfRMNqsbU4sQ3maMVN3S"
access_token = "1270458425063981056-jvtE1ym2vqFCLLt9iWcNsuS2lk6x8j"
access_token_secret = "hVVaARh1MkNkMnSRVhKdXPScfkJhOpdl5IsGf51QV30GX"

# Creating the authentication object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# Setting your access token and secret
auth.set_access_token(access_token, access_token_secret)
# Creating the API object while passing in auth information
api = tweepy.API(auth)

with open('twitter_experimental/FULL_ARCHIVE_TWEETS.csv', 'w', newline='') as csvfile:
    fieldnames = [
        'user',
        'search query', 
        'post date-time', 
        'account status', 
        'account sentiment',
        'account sentiment score', 
        'retweet status', 
        'retweet sentiment',
        'retweet sentiment score',
        'post location', 
        'tweet id', 
        'account subjectivity',
        'account subjectivity score', 
        'retweet subjectivity',
        'retweet subjectivity score'
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    running_count = 0
    with open("twitter_experimental/experimental_output.jsonl", "r") as fptr:
        for json_object in fptr:
            running_count += 1
            # print(json_object)
            json_dic = json.loads(json_object)

            user_handle = json_dic["user"]["screen_name"]
            tweet_id = json_dic["id"]
            query = json_dic["Alan_keyword_query"]

            # obtains status using tweet id
            status = api.get_status(tweet_id, tweet_mode="extended")
            
            # initializing all the fieldnames
            retweet_status = ""
            account_status = ""
            account_sentiment = ""
            retweet_sentiment = ""
            account_sentiment_score = ""
            retweet_sentiment_score = ""
            account_subjectivity = ""
            account_subjectivity_score = ""
            retweet_subjectivity = ""
            retweet_subjectivity_score = ""

            # retweet_exists = False
            # account_exists = False
            try:
                retweet_status = status.retweeted_status.full_text
                # retweet_exists = True
                retweet_list = twitter_nlp.mood_function(retweet_status)
                retweet_sentiment = retweet_list[0]
                retweet_sentiment_score = retweet_list[1]
                retweet_subjectivity_score = retweet_list[2]
                retweet_subjectivity = retweet_list[3]
            except AttributeError:
                account_status = status.full_text
                # account_exists = True
                account_list = twitter_nlp.mood_function(account_status)
                account_sentiment = account_list[0]
                account_sentiment_score = account_list[1]
                account_subjectivity_score = account_list[2]
                account_subjectivity = account_list[3]
                retweet_status = ""
                # retweet_exists = False
                try:
                    retweet_status = status.quoted_status.full_text
                    # retweet_exists = True
                    retweet_list = twitter_nlp.mood_function(retweet_status)
                    retweet_sentiment = retweet_list[0]
                    retweet_sentiment_score = retweet_list[1]
                    retweet_subjectivity_score = retweet_list[2]
                    retweet_subjectivity = retweet_list[3]
                except AttributeError:
                    retweet_status = ""
                    # retweet_exists = False

            writer.writerow({
                'user': user_handle,
                'search query': query,
                'post date-time': status.created_at,
                'account status': account_status,
                'account sentiment': account_sentiment,
                'account sentiment score': account_sentiment_score,
                'retweet status': retweet_status,
                'retweet sentiment': retweet_sentiment,
                'retweet sentiment score': retweet_sentiment_score,
                'post location': status.place, # only available if user adds on IOS or andriod / not on web
                'tweet id': tweet_id,
                'account subjectivity': account_subjectivity,
                'account subjectivity score': account_subjectivity_score,
                'retweet subjectivity': retweet_subjectivity,
                'retweet subjectivity score': retweet_subjectivity_score 
            })
            
            # for every tweet that I get, I will sleep for 1 sec. This means we can do 900 tweets per 15 min,
            # which is the max output for the rate limit twitter sets
            time.sleep(1)
            print(f'Running Count: {running_count}\r', end="")
    print()
    print()
    print(f"{running_count} tweets processed.")
    print("Program finished.")