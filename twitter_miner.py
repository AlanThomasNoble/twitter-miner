import tweepy
import sys
import time
import csv
import sqlite3, os, pandas as pd
from decouple import config

consumer_key = config("consumer_key")
consumer_secret = config("consumer_secret")
access_token = config("access_token")
access_token_secret = config("access_token_secret")

#################################### LIBRARIES FOR NLP ##############################################
import twitter_nlp
#####################################################################################################

############################ LIBRARIES FOR GETTING OLDER TWEETS #####################################
import GetOldTweets3 as got
import sys
from datetime import datetime, timedelta
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
#####################################################################################################


#####################################################################################################
'''Authentication'''
#####################################################################################################

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

def exit_program(err_msg='Manual exit'):
    '''exits software safely'''
    print(f'\n{err_msg}')
    print("Exited program.")
    sys.exit()


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
    query = f'SELECT {params} FROM {fileName}'
    results = pd.read_sql_query(query, conn)
    results.to_csv(f"{fileName}.csv", index=True)
    conn.close()
    print(f'CSV File Generated - {fileName}.csv')


def getInfo(status, t, retweet, func='single_user'):
    '''Outputs Data Based on Status Object'''
    user = status.author.screen_name
    tweet_text = t
    date_time = status.created_at.__str__()
    location = status.place
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
        reply = bool(status.in_reply_to_status_id)
        retweet = False

    if func == 'single_user':
        return tuple((user, tweet_text, date_time, location, ID, hashtags, user_mentions, tweet, quoted, reply, retweet))
    # Add your own if block here for the corresponding function.


#####################################################################################################
'''Mining Functions'''
#####################################################################################################

def obtain_tweets_from_single_user(api, fileName='tweets', append=False):
    '''Outputs a set of given user's tweets'''

    try:
        user_id = input("Enter user's id (Ex: _AVPodcast, selfdriving360, etc.): ")
        print()
        print("Enter -1 if no specific number is desired.")
        number_mine = input("Enter the number of tweets you want to mine from this account: ")
        print()
        print("Obtaining user's tweets...")
        print()
        print("The following tweets are from this account:", user_id)

        # Reset
        if not append:
            os.system(f'rm -rf {fileName}.*')
        conn = sqlite3.connect(f'{fileName}.db')
        c = conn.cursor()

        # Create Table (datatypes: https://www.sqlite.org/datatype3.html)
        if not append:
            c.execute('''CREATE TABLE tweets (
                user TEXT, 
                post_date_time TEXT, 
                account_status TEXT,
                account_sentiment TEXT, 
                account_sentiment_score TEXT, 
                retweet_status TEXT,
                retweet_sentiment TEXT,
                retweet_sentiment_score TEXT,
                post_location TEXT, 
                tweet_id TEXT,
                account_subjectivity TEXT, 
                account_subjectivity_score TEXT, 
                retweet_subjectivity TEXT,
                retweet_subjectivity_score)''')

        # init loop variables
        firstIteration = True; incoming = []; oldest = [];

        runningCount = 0
        # Scraping
        while firstIteration or len(incoming) > 0:
            # Collect First Set of Tweet Objects
            if firstIteration:
                incoming = api.user_timeline(screen_name=user_id,count=200,include_rts=True,tweet_mode='extended')
                firstIteration = False

            # Obtain Full Tweets
            counter = len(incoming)
            for tweet in incoming:
                # storeData(tweet): add function
                time.sleep(1) # Ensure no Runtime Error
                status = api.get_status(tweet.id, tweet_mode="extended") # obtain tweet

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

                query = f"INSERT INTO tweets VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
                data = tuple((
                    status.user.screen_name, 
                    status.created_at, 
                    account_status,
                    account_sentiment, 
                    account_sentiment_score, 
                    retweet_status,
                    retweet_sentiment,
                    retweet_sentiment_score,
                    status.place, 
                    tweet.id,
                    account_subjectivity, 
                    account_subjectivity_score,
                    retweet_subjectivity, 
                    retweet_subjectivity_score))
                c.execute(query, data)

                # Decrement
                counter -= 1
                # Adjust Frame of Reference
                if counter == 0:
                    oldest = tweet.id - 1 # Set equal to last tweet

                # Print Running Count
                runningCount += 1
                print(f'Running Count: {runningCount}\r', end="")

                if(runningCount == int(number_mine)):
                    sys.exit()


            # Update Set of Tweet Objects
            incoming = api.user_timeline(screen_name=user_id,count=200,max_id=oldest,tweet_mode='extended', include_rts=True)

        # Save Data and Close Connection
        conn.commit()
        conn.close()

        print('\nCompleted.')
        print(f'Tweets Retrieved {runningCount}')
        print('SQL File Located in tweets.db')
        convertToCSV(fileName) # Remove as Desired.

    except (KeyboardInterrupt, SystemExit):
        conn.commit()
        conn.close()
        print('\nStopped early or number of tweets wanted has been achieved...')
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
    f_ptr = open(f'input/List_Of_Accounts_input/LOA2.txt', 'r')
    # w_ptr = open(f'output/FULL_TEXT_list_of_accounts_output.txt', 'w')
    
    with open('output/List_Of_Accounts/list_of_accounts_out.csv', 'w', newline='') as csvfile:
        fieldnames = [
            'user', 
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

        # go through each line in the file
        running_count = 0
        for line in f_ptr:
            account = line.rstrip('\n')
            # max number of tweets per accounts is 200
            account_tweets = []
            try:
                account_tweets = api.user_timeline(account, count=num_tweets, include_rts=True)
            except tweepy.TweepError:
                continue
                    
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
                account_status = ""
                account_sentiment = ""
                retweet_sentiment = ""
                account_sentiment_score = ""
                retweet_sentiment_score = ""
                account_subjectivity = ""
                account_subjectivity_score = ""
                retweet_subjectivity= ""
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
                    'user': account,
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
                print(f'Running Count: {running_count}, Account: {account}\r', end="")
        print()
        print("Completed mining via list of accounts.")
        print(f"Tweets generated: {running_count}")
        # w_ptr.write("\n")
        # w_ptr.write("\n")

    f_ptr.close()
    print("Tweets can be found in output/List_Of_Accounts/list_of_accounts_out.csv")


def obtain_tweets_for_weekly_search(api):
    '''Obtains tweets from the past 7 days for a search query list and returns csv with results from query list.

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
    CSV with all the tweets and analystics data
    '''

    num_tweets = input("Enter the number of tweets you would like per keyword in the list (enter >= 5 tweets): ")
    print()
    print("Obtaining tweets from a list of keywords...")
    print()

    # open the file
    # f_ptr = open(f'input/list_of_keywords.txt', 'r')
    f_ptr = open(f'input/weeklySearch_input/list_of_keywords.txt', 'r')
    with open('output/weeklySearch/weeklySearch_out.csv', 'w', newline='') as csvfile:
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

        # go through each line in the file
        running_count = 0
        for query in f_ptr:
            query = query.rstrip('\n')
            tweets = api.search(query, count=int(num_tweets))

            for tweet in tweets:
                running_count += 1
                status = api.get_status(tweet.id, tweet_mode="extended")

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
                    'user': status.user.screen_name,
                    'search query': query,
                    'post date-time': status.created_at,
                    'account status': account_status,
                    'account sentiment': account_sentiment,
                    'account sentiment score': account_sentiment_score,
                    'retweet status': retweet_status,
                    'retweet sentiment': retweet_sentiment,
                    'retweet sentiment score': retweet_sentiment_score,
                    'post location': status.place, # only available if user adds on IOS or andriod / not on web
                    'tweet id': tweet.id,
                    'account subjectivity': account_subjectivity,
                    'account subjectivity score': account_subjectivity_score,
                    'retweet subjectivity': retweet_subjectivity,
                    'retweet subjectivity score': retweet_subjectivity_score 
                })

                # we can only make 900 get status calls -> 1 status call per sec
                # we can only make 180 search api calls -> 1 search api call per 5 sec
                # in every 15 min
                time.sleep(1)
                print(f'Running Count: {running_count}\r', end="")
        print()
        print("Completed mining via weeklySearch.")
        print(f"Tweets generated: {running_count}")
        print("Output can be found in output/weeklySearch/weeklySearch_out.csv.")


def search_no_limits(api, maxtweetperday=5):
    '''Obtains tweets for a search query list and returns csv with results for the query list.

    Requirements
    ------------
    1) Each accound id corresponds to a PUBLIC accounts
    2) Each account id is spelled correctly

    Returns
    -------
    CSV with all the tweets and analystics data
    '''

    sinceDate = input("Enter the search start date (ex: YYYY-MM-DD): ")
    untilDate = input("Enter the search end date (ex: YYYY-MM-DD): ")
    # sinceDate = "2019-01-01"
    # untilDate = "2019-07-01"

    #create a list of day numbers
    since = datetime.strptime(sinceDate, '%Y-%m-%d')
    days = list(range(0, (datetime.strptime(untilDate, '%Y-%m-%d') - datetime.strptime(sinceDate, '%Y-%m-%d')).days+1))

    running_count = 0
    with open('output/Search/out.csv', 'w', newline='') as csvfile:
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
        with open('input/Search_input/LOK.txt', "r") as fptr:
            for query in fptr:
                query = query.rstrip('\n')
                print("Current account: ", query)
                print()
                print()
                for day in days:
                    init = got.manager.TweetCriteria().setQuerySearch(query).setSince((since + timedelta(days=day)).strftime('%Y-%m-%d')).setUntil((since+ timedelta(days=day+1)).strftime('%Y-%m-%d')).setMaxTweets(maxtweetperday)
                    get = got.manager.TweetManager.getTweets(init)

                    for tweet in get:
                        running_count += 1
                        tweet_id = tweet.id

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
                            'user': status.user.screen_name,
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
    print("Completed mining via Search.")
    print(f"Tweets generated: {running_count}")
    print("Output can be found in output/Search/out.csv.")
