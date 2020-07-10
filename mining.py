# External Libraries
import time
import csv
import os
import sys
import tweepy
import sqlite3
import pandas as pd

# Internal Libraries
import twitter_nlp

#####################################################################################################
'''Authentication'''
#####################################################################################################
consumer_key = "e9phIIirNUPdAX8IvMFqQSzDp"
consumer_secret = "4Mnv0GBAWly06Wcf3U4Gzo98tvWqrpdfRMNqsbU4sQ3maMVN3S"
access_token = "1270458425063981056-jvtE1ym2vqFCLLt9iWcNsuS2lk6x8j"
access_token_secret = "hVVaARh1MkNkMnSRVhKdXPScfkJhOpdl5IsGf51QV30GX"

def tweepyAuthentication():
    '''Completes authentication steps for tweepy'''

    # Creating the authentication object
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    # Setting your access token and secret
    auth.set_access_token(access_token, access_token_secret)
    # Creating the API object while passing in auth information
    api = tweepy.API(auth)
    return api




#####################################################################################################
'''Helper Functions'''
#####################################################################################################
def convertToCSV(fileName, params='*'):
    '''Converts DB Files to CSV Format

    Parameters
    ----------
    fileName: str
        Name of File

    params: str
        Specifies selection parameters for SQL 
    '''
    conn = sqlite3.connect(f'{fileName}.db')
    c = conn.cursor()
    query = f'SELECT {params} -FROM {fileName}'
    results = pd.read_sql_query(query, conn)
    results.to_csv(f"{fileName}.csv", index=True)
    conn.close()
    print(f'CSV File Generated - {fileName}.csv')


def getInfo(status, t, retweet, func):
    '''Outputs Data Based on Status Object'''
    user = status.author.screen_name
    tweet_text = t
    date_time = status.created_at.__str__()
    location = status.place
    if location:
        location = f'Loc: {status.place.full_name}, {status.place.country_code} | Coord: {status.place.bounding_box.coordinates}'
        print(location) # remove if desired.
    ID = status.id
    hashtags = ', '.join([h['text'] for h in status.entities['hashtags']])
    user_mentions = ', '.join([t['screen_name'] for t in status.entities['user_mentions']])
    if retweet:
        tweet = False
        quoted = False
        reply = False
        retweet = True
    else:
        tweet = not status.is_quote_status and not bool(status.in_reply_to_status_id)
        quoted = status.is_quote_status
        if quoted:
            quoted_text = None # WIP
        reply = bool(status.in_reply_to_status_id)
        retweet = False

    if func == 'single_user':
        return tuple((user, tweet_text, date_time, location, ID, hashtags, user_mentions, tweet, quoted, reply, retweet))


def storeData(api, tweet, func):
    '''Stores Data for a tweet Entry'''
    time.sleep(1) # Ensure no Runtime Error
    status = api.get_status(tweet.id, tweet_mode="extended")
    try: # check if retweet
        t = status.retweeted_status.full_text
        data = getInfo(status,t,True,func) # Returns a Tuple
        query = f"INSERT INTO tweets VALUES (?,?,?,?,?,?,?,?,?,?,?)"
    except AttributeError: # Not a retweet
        t = status.full_text
        data = getInfo(status,t,False,func) # Returns a Tuple
        query = f"INSERT INTO tweets VALUES (?,?,?,?,?,?,?,?,?,?,?)"
    finally:
        return query, data


def exit_program(err_msg='Invalid Input'):
    '''exits software safely'''
    print(f'\n{err_msg}')
    print("Exited program.")
    sys.exit()




#####################################################################################################
'''Mining Functions'''
#####################################################################################################
def obtain_tweets_from_single_user(api, fileName='tweets', append=False):
    '''Outputs a set of given user's tweets'''
    try:
        user_id = input("Enter user's id (Ex: _AVPodcast, selfdriving360, etc.): ")
        print("\nObtaining user's tweets...")
        print(f"\nThe following tweets are from this account: {user_id}")

        # Delete File Contents if No Append
        if not append:
            os.system(f'rm -rf {fileName}.*')

        # Connection and Cursor Object
        conn = sqlite3.connect(f'{fileName}.db')
        c = conn.cursor()

        # Create Table (datatypes: https://www.sqlite.org/datatype3.html)
        if not append:
            c.execute('''CREATE TABLE tweets (user TEXT, tweet_text TEXT, date_time DATETIME, location TEXT, id INTEGER, hashtags TEXT, user_mentions TEXT, tweet BOOLEAN, quoted BOOLEAN, reply BOOLEAN, retweet BOOLEAN)''')

        # init loop variables
        firstIteration = True; incoming = []; oldest = []; runningCount = 0

        # Scraping
        while firstIteration or len(incoming) > 0:
            # Collect First Set of Tweet Objects
            if firstIteration:
                incoming = api.user_timeline(screen_name=user_id,count=200,include_rts=True,tweet_mode='extended')
                firstIteration = False

            # Set counter
            counter = len(incoming)

            # Store Twitter Data
            for tweet in incoming:
                query, data = storeData(api,tweet,'single_user')
                c.execute(query, data)

                # Decrement
                counter -= 1

                # Adjust Frame of Reference
                if counter == 0:
                    oldest = tweet.id - 1

                # Print Running Count
                runningCount += 1
                print(f'Running Count: {runningCount}\r', end="")

            # Update Set of Tweet Objects
            incoming = api.user_timeline(screen_name=user_id,count=200,max_id=oldest,tweet_mode='extended', include_rts=True)

        # Save Data and Close Connection
        conn.commit()
        conn.close()

        print('\nCompleted.')
        print(f'Tweets Retrieved {runningCount}')
        print(f'SQL File Located in {fileName}.db')
        convertToCSV(fileName) # Remove as Desired.

    except KeyboardInterrupt:
        conn.commit()
        conn.close()
        print('\nStopped Early...')
        print(f'Tweets Retrieved {runningCount}')
        print(f'SQL File Located in {fileName}.db')
        convertToCSV(fileName) # Remove as Desired.
        exit_program()


def PARTIAL_TEXT_tweets_from_list_users(api):
    '''Quickly outputs tweets from a list of users

    Notes: 
        > Can occasionally obtain a PARTIAL TEXT tweet but will QUICKLY run
        > The file containing the list of accounts is found in the input folder

    Requirements
    ------------
    1) Each accound id corresponds to a PUBLIC accounts
    2) Each account id is spelled correctly
    '''

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


def FULL_TEXT_tweets_from_list_users(api):
    '''Outputs FULL TEXT tweets from a list of users

    Notes: 
        > The file containing the list of accounts is found in the input folder
        > WILL OBTAIN FULL TEXT AND RETWEET TEXT BUT WILL TAKE A LONG TIME TO RUN

    Requirements
    ------------
    1) Each accound id corresponds to a PUBLIC accounts
    2) Each account id is spelled correctly
    '''

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
                
                # print(status.place)

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
    '''Obtains tweets from a search query and returns list of json objects for each result from query.

    Notes: 
        > The file containing the list of accounts is found in the input folder
        > WILL OBTAIN FULL TEXT AND RETWEET TEXT BUT WILL TAKE A LONG TIME TO RUN
        > If we have list of keywords, we will be able to generate hundreds of tweets
        > Enter a list of twitter search queries (Ex: Autonomous Vehicles, Self Driving Technology, etc.) in list_of_keywords.txt
        > Keep in mind that the search index has a 7-day limit. In other words, no tweets will be found for a date older than one week.
        > q – the search query string of 500 characters maximum, including operators. Queries may additionally be limited by complexity.

    Requirements
    ------------
    1) Each accound id corresponds to a PUBLIC accounts
    2) Each account id is spelled correctly

    Returns
    -------
    JSON object:
        tweet text, tweet id, tweet hashtag information, and the tweet user information
    '''

    num_tweets = input("Enter the number of tweets you would like per keyword in the list (enter >= 5 tweets): ")
    print()
    print("Obtaining tweets from a list of keywords...")
    print()

    # open the file
    # f_ptr = open(f'input/list_of_keywords.txt', 'r')
    f_ptr = open(f'input/crash_keywords.txt', 'r')
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