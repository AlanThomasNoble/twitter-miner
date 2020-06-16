import tweepy
import sys
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
    print("(2) List - obtain tweets from a list of users")
    print("(3) Search - obtain tweets from a search query")
    print("(4) Limits - prints json of current API usage limits")
    print("(5) Exit - exits software")
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

    # Using the API object to get tweets from a given user's timeline
    # user_tweets = api.lookup_users(user_id)
    user_tweets = api.user_timeline(user_id)
    # foreach through all tweets pulled
    count = 1
    for tweet in user_tweets:
    # printing the text stored inside the tweet object
        pre = "(" + str(count) + ")"
        print(pre, tweet.text)
        print()
        count += 1


# Action: outputs tweets from a list of users
# The file containing the list of accounts is found in the input folder
# Requirements
# 1) Each account id corresponds to a PUBLIC accounts
# 2) Each account id is spelled correctly
def obtain_tweets_from_list_users(api):
    print("Obtaining tweets from a list of users...")
    print()

    # open the file
    f_ptr = open(f'input/list_of_accounts.txt', 'r')

    # go through each line in the file
    running_count = 1
    for line in f_ptr:
        account = line.rstrip('\n')
        account_tweets = api.user_timeline(account)
        #print(account_tweets)
        #exit_program()

        print("The following tweets are from this account: ", account)
        for tweet in account_tweets:
        # printing the text stored inside the tweet object
            pre = "(" + str(running_count) + ")"
            print(pre, tweet.text)
            print()
            running_count += 1
        print()


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
        obtain_tweets_from_list_users(api)
    elif user_input == "Search":
        obtain_tweets_from_search(api)
    elif user_input == "Limits":
        check_limit(api)
    else:
        exit_program()

if __name__ == "__main__":
    main()