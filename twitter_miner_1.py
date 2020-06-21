import tweepy
import sys
import time

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
    # check for '/statuses/user_timeline'
    # check for '/statuses/lookup'
    # check for '/statuses/show/:id'
    # check for '/search/tweets'
    print(api.rate_limit_status())


# Action: outputs a set of a given user's tweets
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
        headers = ['User','Tweet Text','DateTime','ID','Tweet','Quoted','Reply','Retweet']
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
                        'ID': tweet.id,
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
                        'ID': tweet.id,
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
        # max number of tweets per accounts is 200
        account_tweets = api.user_timeline(account, count=num_tweets, include_rts=True)

        account_line  = f"The following tweets are from this account: {account}\n" # +
        # account_line  = "The following tweets are from this account: " + account + "\n"
        w_ptr.write(account_line)

        # status.retweeted can be used to see if the text was retweeted
        for each_tweet in account_tweets:
            running_count += 1
            # obtains tweet id
            tweet_id = each_tweet.id
            # obtains status using tweet id
            status = api.get_status(tweet_id, tweet_mode="extended")

            w_ptr.write(f"{running_count}) {status.created_at}\n")
            # w_ptr.write(str(running_count) + ") " + str(status.created_at) + "\n")
            try:
                w_ptr.write(f"retweet status: {status.retweeted_status.full_text}\n\n") # +
                # w_ptr.write("retweet status: " + status.retweeted_status.full_text + "\n\n")
            except AttributeError:
                w_ptr.write(f"account status: {status.full_text}\n") # +
                # w_ptr.write("account status: " + status.full_text + "\n")
                try:
                    w_ptr.write(f"retweet status: {status.quoted_status.full_text}\n\n") # +
                    # w_ptr.write("retweet status: " + status.quoted_status.full_text + "\n\n")
                except AttributeError:
                    w_ptr.write("\n")
            # for every tweet that I get, I will sleep for 1 sec. This means we can do 900 tweets per 15 min,
            # which is the max output for the rate limit twitter sets
            time.sleep(1)
        print(running_count)

        w_ptr.write("\n")
        w_ptr.write("\n")

    f_ptr.close()
    w_ptr.close()
    print(running_count, "tweets found.")
    print("Tweets can be found in FULL_TEXT_list_of_accounts_output.txt")


# Action: obtains tweets from a search query and returns list of json objects for each result from query
# Return: JSON objects have the tweet text, tweet id, tweet hashtag information, and the tweet user information
# If we have list of keywords, we will be able to generate hundreds of tweets
# Enter a list of twitter search queries (Ex: Autonomous Vehicles, Self Driving Technology, etc.) in list_of_keywords.txt
# IMPORTANT DETAILS:
# Keep in mind that the search index has a 7-day limit. In other words, no tweets will be found for a date older than one week.
# q – the search query string of 500 characters maximum, including operators. Queries may additionally be limited by complexity.
def obtain_tweets_from_search(api):
    num_tweets = input("Enter the number of tweets you would like per keyword in the list: ")
    print()
    print("Obtaining tweets from a list of keywords...")
    print()

    # open the file
    f_ptr = open(f'input/list_of_keywords.txt', 'r')
    w_ptr = open(f'output/keywords_output.txt', 'w')

    # go through each line in the file
    running_count = 0
    for query in f_ptr:
        print("Searching for ", query, " ...")
        print()

        tweets = api.search(query, count=int(num_tweets))
        for tweet in tweets:
            running_count += 1
            status = api.get_status(tweet.id, tweet_mode="extended")
            
            print(f"{running_count}) {status.created_at}\n")
            try:
                print(f"retweet status: {status.retweeted_status.full_text}\n\n") # +
                # w_ptr.write("retweet status: " + status.retweeted_status.full_text + "\n\n")
            except AttributeError:
                print(f"account status: {status.full_text}\n") # +
                # w_ptr.write("account status: " + status.full_text + "\n")
                try:
                    print(f"retweet status: {status.quoted_status.full_text}\n\n") # +
                    # w_ptr.write("retweet status: " + status.quoted_status.full_text + "\n\n")
                except AttributeError:
                    print("\n")

            exit_program()

            # out_json = {}
            # out_json["tweet_id"] = tweet._json["id"]
            # out_json["tweet_text"] = tweet._json["text"]
            # # out_json["tweet_text_truncated"] = tweet._json["truncated"]
            # out_json["tweet_user_info"] = tweet._json["user"]["screen_name"]
            # out_json["tweet_hashtag"] = tweet._json["entities"]["hashtags"]
            # print(out_json)
            # print()
        # we can only make 180 requests every 15 minutes
        time.sleep(5)

        print(f"Number of results printed: {count}") # +
    # print("Number of results printed: ", count)

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