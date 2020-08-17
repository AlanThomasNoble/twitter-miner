import sys, os

#################################### LIBRARIES ######################################################
from twitter_datavis import Visuals
import twitter_miner
#####################################################################################################

def start():
    '''Provides initial output to user'''
    choice = input("What would you like to do today? \n(1) mine\n(2) visuals\tchoice: ")

    if choice == 'mine':
        miningStart()
    elif choice == 'visuals':
        visualsStart()
    else:
        exit_program()


def miningStart():
    '''Initial output for Mining'''
    print("\nThis software will be used to mine Twitter data.\n")
    print("(1) Search - obtain tweets from a search query list (no restrictions)")
    print("(2) weeklySearch - obtain tweets FROM THE LAST 7 DAYS from a search query list")
    print("(3) F_List - obtain tweets from a list of users (guarentees full text)")
    # print("(4) List - obtain tweets from a list of users (cannot guarentee full text)")
    print("(4) User - obtain tweets from a single user")
    print("(5) Limits - prints json of current API usage limits")
    print("(6) Exit - exits software\n")
    user_input = input("Enter the type of data from the above list that you would like to mine (Ex: User, Exit, etc.): ")
    print()

    # List=twitter_miner.PARTIAL_TEXT_tweets_from_list_users,
    validCalls = dict(User=twitter_miner.obtain_tweets_from_single_user,
            F_List=twitter_miner.FULL_TEXT_tweets_from_list_users,
            weeklySearch=twitter_miner.obtain_tweets_for_weekly_search,
            Search=twitter_miner.search_no_limits,
            Limits=check_limit)
    if user_input in validCalls:
        api = twitter_miner.tweepyAuthentication()
        validCalls[user_input](api)
    else:
        exit_program()


def visualsStart():
    '''Initial output for Visuals'''
    print("\nVisualization Types")
    print("(0) plotly")
    print("(1) wordCloud")
    print("(2) ngrams")
    print("(3) polSub")
    print("(4) valueCounts")
    print("(5) intervalGraph")
    print("(6) freqGraph")
    print("(7) toneputs")
    print("(8) wordAnalyzer\n")
    print("Vis (7) Requires Watson Analysis to be Done First to CSV File")
    visType = input("Choose Desired Visualizations (Separate By Commas): ")
    print("\nAvailable Files [Please Do Not Include Extension in Entry (.csv)]: ")
    stream = os.popen('cd output && ls *.csv') # or *.db
    files = stream.read().split()
    [print(f"({files.index(f)+1}) {f}") for f in files]
    fileName = input("Choose FileName to Perform Visualization (i.e. tweets): ")

    # Potential Structural Change (To Decrease User Input in Functions)
    # And Locate all User Input within this Function
    # dict: {analysis: [visualizations]}
    # then in datavis, call each analysis (pass in visualization as a parameter)
    # allow them to editDataframe() beforehand
    # or just generate all possible graphs for a given dataset.

    v = Visuals(fileName, visType)


def check_limit(api):
    '''Returns json showing the current limits of the API calls

    Notes:
        > check for '/statuses/user_timeline'
        > check for '/statuses/lookup'
        > check for '/statuses/show/:id'
        > check for '/search/tweets'
    '''
    print(api.rate_limit_status())


def exit_program(err_msg='Manual Exit'):
    '''Exits software safely'''
    print(f'\n{err_msg}')
    print("Exited program.")
    sys.exit()


def main():
    start()


if __name__ == "__main__":
    main()