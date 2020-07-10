import sys, os

#################################### LIBRARIES ######################################################
from datavis import Visuals
import mining
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
    print("\nThis software will be used to mine Twitter data.")
    print("\n(1) User - obtain a set of a given user's tweets using an account's user ID")
    print("(2) List - quickly retrival of tweets from a list of users (cannot guarentee full text)")
    print("(3) F_List - obtain full text tweets from a list of users")
    print("(4) Search - obtain tweets from a search query")
    print("(5) Limits - prints json of current API usage limits")
    print("(6) Exit - exits software\n")
    user_input = input("Enter the type of data from the above list that you would like to mine (Ex: User, Exit, etc.): ")
    print()

    validCalls = dict(User=mining.obtain_tweets_from_single_user,
            List=mining.PARTIAL_TEXT_tweets_from_list_users,
            F_List=mining.FULL_TEXT_tweets_from_list_users,
            Search=mining.obtain_tweets_from_search,
            Limits=check_limit)
    if user_input in validCalls:
        api = mining.tweepyAuthentication()
        validCalls[user_input](api)
    else:
        exit_program()


def visualsStart():
    '''Initial output for Visuals'''
    print("\nVisualization Types")
    print("(1) wordCloud")
    print("(2) ngrams")
    print("(3) polSub (WIP)")
    print("(4) valueCounts")
    print("(5) analytics")
    print("(6) freqGraph\n")
    visType = input("Choose Desired Visualizations (Separate By Commas): ")
    print("Available Files [Please Do Not Include Extension in Entry (.csv)]: ")
    stream = os.popen('cd output && ls *.csv') # or *.db
    files = stream.read().split()
    [print(f"({files.index(f)+1}) {f}") for f in files]
    fileName = input("Choose FileName to Perform Visualization (i.e. tweets): ")
    print("\nAdditional Specifications ('select' or 'pass'): ")
    dateChoice = input("Would you like to analyze tweets from certain dates? ")
    start_date = None; end_date = None
    if dateChoice == 'select':
        start_date = input("Select a start date [yyyy-mm-dd hh:mm:ss] (Time is Optional): ")
        end_date = input("Select an end date [yyyy-mm-dd hh:mm:ss] (Time is Optional): ")
    print()
    kwargs = dict(start_date=start_date, end_date=end_date) # add more as needed.
    kwargs = dict(filter(lambda k: k[1], kwargs.items())) # Remove all None

    try:
        v = Visuals(fileName, visType, **kwargs)
    except ValueError:
        exit_program()


def check_limit(api):
    '''Returns json showing the current limits of the API calls

    Notes:
        > check for '/statuses/user_timeline'
        > check for '/statuses/lookup'
        > check for '/statuses/show/:id'
        > check for '/search/tweets'
    '''
    print(api.rate_limit_status())


def exit_program(err_msg='Invalid Input'):
    '''Exits software safely'''
    print(f'\n{err_msg}')
    print("Exited program.")
    sys.exit()


def main():
    start()


if __name__ == "__main__":
    main()