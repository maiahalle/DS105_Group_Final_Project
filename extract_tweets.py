# import the required libraries
import requests
from requests.adapters import HTTPAdapter, Retry
import pandas
import json
import spacy
import time
from collections import Counter
import config
import os

# Storing and defining URL
base_url = "https://api.twitter.com/2/"

# build url to retrieve all recent tweets for a user
def create_tweet_url(user_id):
    return "{}users/{}/tweets".format(base_url, user_id)

# build the url to find user ids from a twitter handle
def create_userid_url(user_handle):
    return "{}users/by/username/{}".format(base_url, user_handle)

# create dictionary to get required fields for tweets and return maximum number of rows per request
def get_params():
    return {"tweet.fields":
                "id,text,author_id,conversation_id,created_at,in_reply_to_user_id,lang,possibly_sensitive,public_metrics",
            "max_results": 100}
    
# build the header needed to gain access with the Bearer token stored in the config file
def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {config.bearer_token}"
    r.headers["User-Agent"] = "LSE-WordCounter"
    return r

# call twitter api with request url and parameters and return the response in json
def connect_to_endpoint(url, params):
    session = requests.Session()
    # configure retrying with a pause for half a minute
    retry = Retry(connect=10, backoff_factor=30)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    return response.json()

# find and return the twitter id based on passed twitter handle
# error handling: if no id is found return None and print an error message
def get_twitter_id(handle):
    json_response = connect_to_endpoint(create_userid_url(handle), None)

    # error checking in case a twitter handle can't be found
    if json_response and "data" in json_response:
        return {"id": json_response["data"]["id"],
                "name": json_response["data"]["name"]}
    else:
        print("Error: id not found for ", handle)
        return None

# convert tweet data into a dictionary of name value pairs 
def get_tweet_dict(tweet, handle, name):
    metrics = tweet["public_metrics"]
    return {"handle": handle,
            "name": name,
            "tweet_id": tweet["id"],
            "author_id": tweet["author_id"],
            "lang": tweet["lang"],
            "replied_to": ",".join(tweet['edit_history_tweet_ids']),
            'created_at': tweet['created_at'],
            'tweet_text': tweet['text'],
            'possibly_sensitive': tweet['possibly_sensitive'],
            'conversation_id': tweet['conversation_id'],
            "retweet_count": metrics["retweet_count"],
            "reply_count": metrics["reply_count"],
            "like_count": metrics["reply_count"],
            "quote_count": metrics["quote_count"]}

# get all tweets for a twitter handle
# returns a tweet data in a dataframe
# if there are not tweets an empty dataframe will be returned
def get_tweets(handle):
    # initialize list to hold all the tweet dictionaries
    dict_list = []
    csv_filename = "csv_cache/{}.csv".format(handle)
    if os.path.isfile(csv_filename):
        print ("loaded tweets from file for ", handle)
        return pandas.read_csv(csv_filename)

    id_dict = get_twitter_id(handle)
    if id_dict is None:
        # return an empty DataFrame
        return pandas.DataFrame(dict_list)

    print("get tweets for ", handle)
    url = create_tweet_url(id_dict["id"])
    params = get_params()
    # get first page
    json_response = connect_to_endpoint(url, params)

    # while there is data to process, extract tweet data
    while json_response and "data" in json_response:
        # use extend function to merge tweets with previous dicts
        dict_list.extend([get_tweet_dict(tweet, handle, id_dict["name"]) for tweet in json_response["data"]])
        if "next_token" not in json_response["meta"]:
            break
        params['pagination_token'] = json_response["meta"]["next_token"]
        json_response = connect_to_endpoint(url, params)
    
    df = pandas.DataFrame(dict_list)
    if len(dict_list):
        print ("saving {} tweets to {}".format(len(dict_list), csv_filename))
        df.to_csv(csv_filename, encoding='utf-8', index=False)
    return df

nlp = spacy.load("en_core_web_sm")
# since we are only looking for tokens we can turn off parsing and turn on sentencizer
nlp.disable_pipe("parser")
nlp.add_pipe("sentencizer")
# include adjectives, nouns, propernouns, verbs and adverbs 
include_types = ["ADJ", "NOUN", "PROPN", "VERB", "ADV"]
# exclude RT: retweet and amp: & (and)
exclude_words = ["rt", "amp"]
def get_tokens(doc):
    return [token.lemma_.lower() for token in doc if token.is_alpha and token.pos_ in include_types and token.lemma_.lower() not in exclude_words]

# Adding new coloumn into the dataframe called word count
def add_word_count(row):
    word_freq = Counter(row["key_word_list"])
    common_words = word_freq.most_common(50)
    df = pandas.DataFrame(common_words, columns = ['Word', 'Count'])
    df["handle"] = row["handle"]
    return df[["handle","Word","Count"]]

def group_tweets(df_tweets, group_filename):
    print("creating summary grouping by handle")
    df_grouped = df_tweets.groupby('handle',as_index=False).agg({'tweet_text': 'count','key_word_list': 'sum'})

    #rename columns
    df_grouped.rename(columns = {'tweet_text':'tweet_count'}, inplace = True)
    df_grouped.to_csv(group_filename, encoding='utf-8', index=False)
    return df_grouped

def count_words(word_count_filename, df_grouped):
    print("get most frequent words")
    df_word_count = pandas.concat([add_word_count(row) for index, row in df_grouped.iterrows()])
    df_word_count.to_csv(word_count_filename, encoding='utf-8', index=False)
    return df_word_count
        
# main function to return dictionary of dataframes and generate csv files
def get_tweet_dfs(acct_file):

    tweet_filename = "tweets.csv"
    group_filename = "grouped.csv"
    word_count_filename = "word_count.csv"
    
    if os.path.isfile(tweet_filename):
        print ("loading all tweets from file")
        df_tweets = pandas.read_csv(tweet_filename, low_memory=False)
        if os.path.isfile(group_filename):
            print ("loading summary grouping from file")
            df_grouped = pandas.read_csv(group_filename, low_memory=False)
        else:
            df_grouped = group_tweets(df_tweets, group_filename)
            
        if os.path.isfile(word_count_filename):
            print ("loading all word counts from file")
            df_word_count = pandas.read_csv(word_count_filename, low_memory=False)
        else:
            df_word_count = count_words(word_count_filename, df_grouped)
    else:
        # regenerate all output files
        df_politicians = pandas.read_csv(acct_file)

        print("Start load tweets")
        df_tweets = pandas.concat([get_tweets(handle) for handle in df_politicians["handle"]])

        print("process tweets and generate key words")
        # Remove any rows that have blank tweets
        df_tweets = df_tweets[df_tweets.tweet_text.notna()]
        # add key_word_list column from a list this is faster using the pipe to reduce loading loading times
        df_tweets['key_word_list'] = [get_tokens(doc) for doc in nlp.pipe(df_tweets.tweet_text)]
        df_tweets.to_csv(tweet_filename, encoding='utf-8', index=False)

        df_grouped = group_tweets(df_tweets, group_filename)
        df_word_count = count_words(word_count_filename, df_grouped)

    return {"tweets_df": df_tweets, "summary_df": df_grouped, "freq_words_df": df_word_count}


#call main function for debug
df_dict = get_tweet_dfs("reptweets.csv")
