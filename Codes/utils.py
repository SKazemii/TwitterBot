from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import tweepy
import config, json, os
import pandas as pd
import logging

from pathlib import Path as Pathlb


def create_logger(level):
    loggerName = Pathlb(__file__).stem
    Pathlb(config.log_path).mkdir(parents=True, exist_ok=True)
    grey = "\x1b[38;21m"
    blue = "\x1b[38;5;39m"
    yellow = "\x1b[38;5;226m"
    red = "\x1b[38;5;196m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    logger = logging.getLogger(loggerName)
    logger.setLevel(level)
    t1 = ( blue + "[%(asctime)s]-" + yellow + "[%(name)s @%(lineno)d]" + reset + blue + "-[%(levelname)s]" + reset + bold_red )
    t2 = "%(message)s" + reset
    # breakpoint()
    formatter_colored = logging.Formatter(t1 + t2, datefmt="%m/%d/%Y %I:%M:%S %p ")
    formatter = logging.Formatter(
        "[%(asctime)s]-[%(name)s @%(lineno)d]-[%(levelname)s]      %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p ",)
    file_handler = logging.FileHandler(os.path.join(config.log_path, loggerName + "_loger.log"), mode="w")
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)

    stream_handler.setFormatter(formatter_colored)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger

logger = create_logger(logging.DEBUG)


def sentimentanalyzer(text):
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)
    return scores['pos'], scores['neg'], scores['neu']

def tweeter_API():
    '''Returns a tweepy API object.'''
    auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_token_secret)

    return tweepy.API(auth)

def get_tweets(username, tweet_amount):
    '''Returns a list of tweets from a user's timeline.'''
    api = tweeter_API()
    tweets_dict = api.user_timeline(username, count=tweet_amount)
    return tweets_dict

def get_tweets_from_file(filename):
    '''Returns a list of tweets from a json file for test.'''
    with open(filename, 'r') as f:
        tweets_dict = json.load(f)
    return tweets_dict

def get_tweets_dataframe(tweets_dict):
    '''Returns a pandas DataFrame from a list of tweets.'''
    tweets_list = []
    # Extracting conversation threads for each tweet
    for tweet in tweets_dict['statuses']:
        
        temp = [tweet['created_at'], tweet['user']['name'], tweet['text']]
        tweets_list.append(temp)

    # Create a DataFrame from the tweet data
    Data_frame = pd.DataFrame(data=tweets_list, columns=['created_at', 'user', 'text'])
    Data_frame['pos'], Data_frame['neg'], Data_frame['neu'] = zip(*Data_frame['text'].apply(sentimentanalyzer))

    return Data_frame


def report(Data_frame):
    pass

def save_data(Data_frame):
    '''Saves a pandas DataFrame to a parquet file.'''
    Data_frame.to_parquet(config.data_path + '/tweets.parquet', index=False)

def load_data():
    '''Returns a pandas DataFrame from a parquet file.'''
    Data_frame = pd.read_parquet(config.data_path + '/tweets.parquet')
    return Data_frame