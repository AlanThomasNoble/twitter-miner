import tweepy
import sys
import time
import csv
from csv import DictWriter # Currently Needed for User Function Code (otherwise reference to csv would be needed)

consumer_key = "e9phIIirNUPdAX8IvMFqQSzDp"
consumer_secret = "4Mnv0GBAWly06Wcf3U4Gzo98tvWqrpdfRMNqsbU4sQ3maMVN3S"
access_token = "1270458425063981056-jvtE1ym2vqFCLLt9iWcNsuS2lk6x8j"
access_token_secret = "hVVaARh1MkNkMnSRVhKdXPScfkJhOpdl5IsGf51QV30GX"

#################################### LIBRARIES FOR NLP ##############################################
import twitter_nlp

#####################################################################################################


# Provides initial output to the user
def start():
    print()
    print("This software will be used to mine Twitter data.")
    print()
    print("(1) User - obtain a set of a given user's tweets using an account's user ID")
    print("(2) List - quickly retrival of tweets from a list of users (cannot guarentee full text)")
    print("(3) F_List - obtain full text tweets from a list of users")
    print("(4) Search - obtain tweets from a search query")
    print("(5) Limits - prints json of current API usage limits")
    print("(6) Exit - exits software")
    print()
    data = input("Enter the type of data from the above list that you would like to mine (Ex: User, Exit, etc.): ")
    print()
    return data


# Returns json showing the current limits of the API calls
def check_limit(api):
    # check for '/statuses/user_timeline'
    # check for '/statuses/lookup'
    # check for '/statuses/show/:id'
    # check for '/search/tweets'
    print(api.rate_limit_status())


# Action: outputs a set of a given user's tweets
def obtain_tweets_from_single_user(api):
    user_id = input("Enter user's id (Ex: _AVPodcast, selfdriving360, etc.): ")
    print()
    print("Obtaining user's tweets...")
    print()
    print("The following tweets are from this account:", user_id)

    # Open File
    with open('tweets.csv','w') as file:
        # Initialize Headers and Writer Object
        headers = ['User','Tweet Text','DateTime','Location','ID','Hashtags','User Mentions','Tweet','Quoted','Reply','Retweet']
        csv_writer = DictWriter(file,fieldnames=headers)
        csv_writer.writeheader()

        ## Scraping
        # Initialize Variables
        firstIteration = True # overrides first iteration
        incoming = []; oldest = []; numTweets = 0
        # Loop Through
            # > user_timeline is limited to 200 tweet retrieval
            # > use while loop to bypass and reach twitter max of 3240 tweet retrieval
        while firstIteration or len(incoming) > 0:
            # Collect First Set of Tweet Objects
            if firstIteration:
                incoming = api.user_timeline(screen_name=user_id,count=200,include_rts=True) # include rts in both?, why didn't you move this outside of while?
                firstIteration = False

            # Increment Total Tweets
            numTweets += len(incoming)

            # Obtain Full Tweets
            counter = len(incoming)
            for tweet in incoming:
                time.sleep(1.2) # Ensure no Runtime Error
                status = api.get_status(tweet.id, tweet_mode="extended") # obtain tweet
                try: # check if retweet
                    t = status.retweeted_status.full_text
                    csv_writer.writerow({
                        'User': user_id,
                        'Tweet Text': t,
                        'DateTime': status.created_at.__str__(),
                        'Location': status.place,
                        'ID': tweet.id,
                        'Hashtags': [h['text'] for h in tweet.entities['hashtags']],
                        'User Mentions': [t['screen_name'] for t in tweet.entities['user_mentions']],
                        'Tweet': False,
                        'Quoted': False,
                        'Reply': False,
                        'Retweet': True
                    })
                except AttributeError: # Not a retweet
                    t = status.full_text
                    csv_writer.writerow({
                        'User': user_id,
                        'Tweet Text': t,
                        'DateTime': status.created_at.__str__(),
                        'Location': status.place,
                        'ID': tweet.id,
                        'Hashtags': [h['text'] for h in tweet.entities['hashtags']],
                        'User Mentions': [t['screen_name'] for t in tweet.entities['user_mentions']],
                        'Tweet': not status.is_quote_status and not bool(status.in_reply_to_status_id), 
                        'Quoted': status.is_quote_status,
                        'Reply': bool(status.in_reply_to_status_id),
                        'Retweet': False
                    })
                # Decrement
                counter -= 1
                # Adjust Frame of Reference
                if counter == 0:
                    oldest = tweet.id - 1 # set equal to last tweet

            # Update Set of Tweet Objects
            incoming = api.user_timeline(screen_name=user_id,count=200,max_id=oldest,tweet_mode='extended')

        print(f"Tweets Retrieved {numTweets}")


# Action: quickly outputs tweets from a list of users
# Can occasionally obtain a PARTIAL TEXT tweet but will QUICKLY run
# The file containing the list of accounts is found in the input folder
# Requirements
# 1) Each account id corresponds to a PUBLIC accounts
# 2) Each account id is spelled correctly
def PARTIAL_TEXT_tweets_from_list_users(api):
    print("Obtaining tweets from a list of users...")
    print()

    # open the file
    f_ptr = open(f'input/list_of_accounts.txt', 'r')
    w_ptr = open(f'output/PARTIAL_TEXT_list_of_accounts_output.txt', 'w')

    # go through each line in the file
    running_count = 1
    for line in f_ptr:
        account = line.rstrip('\n')
        account_tweets = api.user_timeline(account)

        account_line  = f"The following tweets are from this account: {account}\n" # +
        w_ptr.write(account_line)

        for tweet in account_tweets:
        # printing the text stored inside the tweet object
            written_tweet = f'{running_count}) {tweet.text}\n\n' # +
            w_ptr.write(written_tweet)
            running_count += 1
        w_ptr.write("\n")

    f_ptr.close()
    w_ptr.close()
    print("Tweets can be found in PARTIAL_TEXT_list_of_accounts_output.txt")


# Action: outputs FULL TEXT tweets from a list of users
# The file containing the list of accounts is found in the input folder
# WILL OBTAIN FULL TEXT AND RETWEET TEXT BUT WILL TAKE A LONG TIME TO RUN
# Requirements
# 1) Each account id corresponds to a PUBLIC accounts
# 2) Each account id is spelled correctly
def FULL_TEXT_tweets_from_list_users(api):
    num_tweets = input("Enter the number of tweets you would like per user in the list: ")
    print()
    print("Obtaining tweets from a list of users...")
    print()

    # open the file
    f_ptr = open(f'input/list_of_accounts.txt', 'r')
    # w_ptr = open(f'output/FULL_TEXT_list_of_accounts_output.txt', 'w')
    
    with open('output/FULL_TEXT_LIST.csv', 'w', newline='') as csvfile:
        fieldnames = [
            'user', 
            'post date-time', 
            'account status', 
            'account sentiment', 
            'retweet status', 
            'retweet sentiment',
            'post location', 
            'tweet id', 
            'account subjectivity', 
            'retweet subjectivity'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # go through each line in the file
        running_count = 0
        for line in f_ptr:
            account = line.rstrip('\n')
            # max number of tweets per accounts is 200
            account_tweets = api.user_timeline(account, count=num_tweets, include_rts=True)

            # status.retweeted can be used to see if the text was retweeted
            for each_tweet in account_tweets:
                running_count += 1
                # obtains tweet id
                tweet_id = each_tweet.id
                # obtains status using tweet id
                status = api.get_status(tweet_id, tweet_mode="extended")
                print(status.place)

                # w_ptr.write(f"{running_count}) {status.created_at}\n")
                # w_ptr.write(str(running_count) + ") " + str(status.created_at) + "\n")
                retweet_status = ""
                retweet_exists = False
                account_status = ""
                account_exists = False
                account_sentiment = ""
                retweet_sentiment = ""
                account_subjectivity = ""
                retweet_subjectivity = ""

                try:
                    retweet_status = status.retweeted_status.full_text
                    retweet_exists = True
                    retweet_sentiment = twitter_nlp.mood_function(retweet_status)[0]
                    retweet_subjectivity = twitter_nlp.mood_function(retweet_status)[2]
                except AttributeError:
                    account_status = status.full_text
                    account_exists = True
                    account_sentiment = twitter_nlp.mood_function(account_status)[0]
                    account_subjectivity = twitter_nlp.mood_function(account_status)[2]
                    retweet_status = ""
                    retweet_exists = False
                    try:
                        retweet_status = status.quoted_status.full_text
                        retweet_exists = True
                        retweet_sentiment = twitter_nlp.mood_function(retweet_status)[0]
                        retweet_subjectivity = twitter_nlp.mood_function(retweet_status)[2]
                    except AttributeError:
                        retweet_status = ""
                        retweet_exists = False

                writer.writerow({
                    'user': account,
                    'post date-time': status.created_at,
                    'account status': account_status,
                    'account sentiment': account_sentiment,
                    'retweet status': retweet_status,
                    'retweet sentiment': retweet_sentiment,
                    'post location': status.place, # only available if user adds on IOS or andriod / not on web
                    'tweet id': tweet_id,
                    'account subjectivity': account_subjectivity,
                    'retweet subjectivity': retweet_subjectivity 
                })
                
                # for every tweet that I get, I will sleep for 1 sec. This means we can do 900 tweets per 15 min,
                # which is the max output for the rate limit twitter sets
                time.sleep(1)
            print(running_count, "tweets collected")

        # w_ptr.write("\n")
        # w_ptr.write("\n")

    f_ptr.close()
    print(running_count, "tweets generated.")
    print("Tweets can be found in FULL_TEXT_LIST.csv")


# Action: obtains tweets from a search query and returns list of json objects for each result from query
# Return: JSON objects have the tweet text, tweet id, tweet hashtag information, and the tweet user information
# If we have list of keywords, we will be able to generate hundreds of tweets
# Enter a list of twitter search queries (Ex: Autonomous Vehicles, Self Driving Technology, etc.) in list_of_keywords.txt
# IMPORTANT DETAILS:
# Keep in mind that the search index has a 7-day limit. In other words, no tweets will be found for a date older than one week.
# q – the search query string of 500 characters maximum, including operators. Queries may additionally be limited by complexity.
def obtain_tweets_from_search(api):
    num_tweets = input("Enter the number of tweets you would like per keyword in the list (enter >= 5 tweets): ")
    print()
    print("Obtaining tweets from a list of keywords...")
    print()

    # open the file
    f_ptr = open(f'input/list_of_keywords.txt', 'r')

    with open('output/KEYWORD_SEARCH_OUTPUT.csv', 'w', newline='') as csvfile:
        fieldnames = [
            'user',
            'search query', 
            'post date-time', 
            'account status', 
            'account sentiment', 
            'retweet status', 
            'retweet sentiment',
            'post location', 
            'tweet id', 
            'account subjectivity', 
            'retweet subjectivity'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # go through each line in the file
        running_count = 0
        for query in f_ptr:

            tweets = api.search(query, count=int(num_tweets))

            for tweet in tweets:
                running_count += 1
                status = api.get_status(tweet.id, tweet_mode="extended")

                # initializing all the fieldnames
                retweet_status = ""
                retweet_exists = False
                account_status = ""
                account_exists = False
                account_sentiment = ""
                retweet_sentiment = ""
                account_subjectivity = ""
                retweet_subjectivity = ""

                try:
                    retweet_status = status.retweeted_status.full_text
                    retweet_exists = True
                    retweet_sentiment = twitter_nlp.mood_function(retweet_status)[0]
                    retweet_subjectivity = twitter_nlp.mood_function(retweet_status)[2]
                except AttributeError:
                    account_status = status.full_text
                    account_exists = True
                    account_sentiment = twitter_nlp.mood_function(account_status)[0]
                    account_subjectivity = twitter_nlp.mood_function(account_status)[2]
                    retweet_status = ""
                    retweet_exists = False
                    try:
                        retweet_status = status.quoted_status.full_text
                        retweet_exists = True
                        retweet_sentiment = twitter_nlp.mood_function(retweet_status)[0]
                        retweet_subjectivity = twitter_nlp.mood_function(retweet_status)[2]
                    except AttributeError:
                        retweet_status = ""
                        retweet_exists = False

                writer.writerow({
                    'user': status.user.screen_name,
                    'search query': query,
                    'post date-time': status.created_at,
                    'account status': account_status,
                    'account sentiment': account_sentiment,
                    'retweet status': retweet_status,
                    'retweet sentiment': retweet_sentiment,
                    'post location': status.place, # only available if user adds on IOS or andriod / not on web
                    'tweet id': tweet.id,
                    'account subjectivity': account_subjectivity,
                    'retweet subjectivity': retweet_subjectivity 
                })

                # we can only make 900 get status calls -> 1 status call per sec
                # we can only make 180 search api calls -> 1 search api call per 5 sec
                # in every 15 min
                time.sleep(1)
            print(running_count, "tweets collected...")
        print(f"{running_count} tweets generated")
        print("Output can be found in KEYWORD_SEARCH_OUTPUT.csv.")
 

# Action: exits software
def exit_program():
    print("Exited program.")
    sys.exit()


def main():
    # Basis of the Twitter App
    # Creating the authentication object
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    # Setting your access token and secret
    auth.set_access_token(access_token, access_token_secret)
    # Creating the API object while passing in auth information
    api = tweepy.API(auth)

    # Outputs initial messages to the user
    user_input = start()

    if user_input == "User":
        obtain_tweets_from_single_user(api)
    elif user_input == "List":
        PARTIAL_TEXT_tweets_from_list_users(api)
    elif user_input == "F_List":
        FULL_TEXT_tweets_from_list_users(api)
    elif user_input == "Search":
        obtain_tweets_from_search(api)
    elif user_input == "Limits":
        check_limit(api)
    else:
        exit_program()

if __name__ == "__main__":
    main()