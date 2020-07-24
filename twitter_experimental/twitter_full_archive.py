CONSUMER_KEY = "e9phIIirNUPdAX8IvMFqQSzDp"
CONSUMER_SECRET = "4Mnv0GBAWly06Wcf3U4Gzo98tvWqrpdfRMNqsbU4sQ3maMVN3S"
DEV_ENVIRONMENT_LABEL = 'experiment'
API_SCOPE = 'fullarchive'  # 'fullarchive' for full archive, '30day' for last 31 days

RESULTS_PER_CALL = 100  # 100 for sandbox, 500 for paid tiers
TO_DATE = '2020-07-01' # format YYYY-MM-DD HH:MM (hour and minutes optional)
FROM_DATE = '2019-11-01'  # format YYYY-MM-DD HH:MM (hour and minutes optional)

MAX_RESULTS = 950  # Number of Tweets you want to collect

FILENAME = 'twitter_experimental/experimental_output.jsonl'  # Where the Tweets should be saved

# Script prints an update to the CLI every time it collected another X Tweets
PRINT_AFTER_X = 100

#--------------------------- STOP -------------------------------#

import yaml
config = dict(
    search_tweets_api=dict(
        account_type='premium',
        endpoint=f"https://api.twitter.com/1.1/tweets/search/{API_SCOPE}/{DEV_ENVIRONMENT_LABEL}.json",
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET
    )
)

with open('twitter_experimental/twitter_keys.yaml', 'w') as config_file:
    yaml.dump(config, config_file, default_flow_style=False)

    
import json
from searchtweets import load_credentials, gen_rule_payload, ResultStream

premium_search_args = load_credentials("twitter_experimental/twitter_keys.yaml",
                                       yaml_key="search_tweets_api",
                                       env_overwrite=False)

n = 0
with open(FILENAME, 'a', encoding='utf-8') as f:
    f_ptr = open(f'input/list_of_keywords_2.txt', 'r')
    for query in f_ptr:
        query = query.rstrip('\n')
        rule = gen_rule_payload(query,
                                results_per_call=RESULTS_PER_CALL,
                                from_date=FROM_DATE,
                                to_date=TO_DATE
                                )

        rs = ResultStream(rule_payload=rule,
                        max_results=MAX_RESULTS,
                        **premium_search_args)

        for tweet in rs.stream():
            n += 1
            if n % PRINT_AFTER_X == 0:
                print('{0}: {1}'.format(str(n), tweet['created_at']))
                print(f"Running count: {n}")
            tweet["Alan_keyword_query"] = query 
            json.dump(tweet, f)
            f.write('\n')
print()
print(f"Running count: {n}")
print('done')