import tweepy
import sys
import time
import pdb
consumer_key = "e9phIIirNUPdAX8IvMFqQSzDp"
consumer_secret = "4Mnv0GBAWly06Wcf3U4Gzo98tvWqrpdfRMNqsbU4sQ3maMVN3S"
access_token = "1270458425063981056-jvtE1ym2vqFCLLt9iWcNsuS2lk6x8j"
access_token_secret = "hVVaARh1MkNkMnSRVhKdXPScfkJhOpdl5IsGf51QV30GX"

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
    print(api.rate_limit_status())


# Action: outputs a set of a given user's tweets
def obtain_tweets_from_single_user(api):
    user_id = input("Enter user's id (Ex: _AVPodcast, selfdriving360, etc.): ")
    print()
    print("Obtaining user's tweets...")
    print()
    print("The following tweets are from this account:", user_id)

    # Import
    from csv import DictWriter

    # Open File
    with open('tweets.csv','w') as file:
        # Initialize Headers and Writer Object
        headers = ['User', 'Tweet', 'ID'] # add more headers...i.e. tweet type (reply, quote, rt)
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
                incoming = api.user_timeline(screen_name=user_id,count=200,include_rts=True)
            else:
                incoming = api.user_timeline(screen_name=user_id,count=200,max_id=oldest,tweet_mode='extended')

            # Increment Total Tweets
            numTweets += len(incoming)

            # Set First Iteration Equal to False
            firstIteration = False

            # Obtain Full Tweets
            counter = len(incoming)
            for tweet in incoming:
                # Alternative Method to reduce get_status() calls [not tested]
                '''
                if "RT @" in tweet.text:
                    time.sleep(1.2)
                    status = api.get_status(tweet.id, tweet_mode="extended") # obtain tweet
                    t = status.retweeted_status.full_text
                    csv_writer.writerow({
                        'User': user_id,
                        'Tweet': t,
                        'ID': tweet.id
                    })
                else:
                    csv_writer.writerow({
                        'User': user_id,
                        'Tweet': t,
                        'ID': tweet.text
                    })
                '''

                time.sleep(1.2) # Ensure no Runtime Error
                status = api.get_status(tweet.id, tweet_mode="extended") # obtain tweet
                try: # check if retweet
                    t = status.retweeted_status.full_text
                    csv_writer.writerow({
                        'User': user_id,
                        'Tweet': t,
                        'ID': tweet.id
                    })
                except AttributeError: # Not a retweet
                    t = status.full_text
                    csv_writer.writerow({
                        'User': user_id,
                        'Tweet': t,
                        'ID': tweet.id
                    })
                # Decrement
                counter -= 1
                # Adjust Frame of Reference
                if not counter:
                    oldest = tweet.id # set equal to last tweet

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

        account_line  = "The following tweets are from this account: " + account + "\n"
        w_ptr.write(account_line)

        for tweet in account_tweets:
        # printing the text stored inside the tweet object
            written_tweet = str(running_count) + ") " + tweet.text + "\n\n"
            w_ptr.write(written_tweet)
            running_count += 1
        w_ptr.write("\n")

    f_ptr.close()
    w_ptr.close()
    print("Tweets can be found in PARTIAL_TEXT_list_of_accounts_output.txt")


# Action: outputs FULL TEXT tweets from a list of users
# The file containing the list of accounts is found in the input folder
# WILL OBTAIN FULL TEXT BUT WILL TAKE A LONG TIME TO RUN
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
    w_ptr = open(f'output/FULL_TEXT_list_of_accounts_output.txt', 'w')

    # go through each line in the file
    running_count = 0
    for line in f_ptr:
        account = line.rstrip('\n')
        account_tweets = api.user_timeline(account, count=num_tweets, include_rts=True)

        account_line  = "The following tweets are from this account: " + account + "\n"
        w_ptr.write(account_line)

        # status.retweeted can be used to see if the text was retweeted
        for each_tweet in account_tweets:
            running_count += 1
            # obtains tweet id
            tweet_id = each_tweet.id
            # obtains status using tweet id
            status = api.get_status(tweet_id, tweet_mode="extended")
            try:
                w_ptr.write(str(running_count) + ") retweeted: " + status.retweeted_status.full_text + "\n")
            except AttributeError:  # Not a Retweet
                w_ptr.write(str(running_count) + ") " + status.full_text + "\n")
            # written_tweet = str(running_count) + ") " + status.full_text + "\n\n"
            # w_ptr.write(written_tweet)
        # w_ptr.write("\n")
        w_ptr.write("\n")
        w_ptr.write("\n")

    f_ptr.close()
    w_ptr.close()
    print(running_count, "tweets found.")
    print("Tweets can be found in FULL_TEXT_list_of_accounts_output.txt")


# Action: obtains tweets from a search query and returns list of json objects for each result from query
# Return: JSON objects have the tweet text, tweet id, tweet hashtag information, and the tweet user information
# If we have list of keywords, we will be able to generate hundreds of tweets
def obtain_tweets_from_search(api):
    search_query = input("Enter a twitter search query (Ex: Autonomous Vehicles, Self Driving Technology, etc.): ")
    num = input("Enter the number of results you would like: ")
    print()

    print("Searching for ", search_query, " ...")
    print()

    tweets = api.search(search_query, count=int(num))
    count = 0
    for tweet in tweets:
        # print(tweet._json["text"])
        # sample json - we can change later
        out_json = {}
        out_json["tweet_id"] = tweet._json["id"]
        out_json["tweet_text"] = tweet._json["text"]
        # out_json["tweet_text_truncated"] = tweet._json["truncated"]
        out_json["tweet_user_info"] = tweet._json["user"]["screen_name"]
        out_json["tweet_hashtag"] = tweet._json["entities"]["hashtags"]

        print(out_json)

        count += 1
        print()

    print("Number of results printed: ", count)

    # how much data?
    # how should json look like


#Add Function for finding list of accounts related to Autonomous Vehicles


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