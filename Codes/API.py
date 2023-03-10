from flask import Flask
from flask_restful import Resource, Api

import utils
import pandas as pd


app = Flask(__name__)
api = Api(app)


accounts_names = ['cathiedwood', 'ylecun', 'taylorlorenz']
tweet_amount = 1000

# index endpoint
class index(Resource):
    def get(self):
        return {'/accounts': 'return a json list of all tracked accounts.',
                '/tweets/<twitter-handle>': "return a json of the user's conversation threads since start.",
                "/audience/<twitter-handle>" : "return a json of information about the audience for a user's account.",
                "/sentiment/<twitter-handle>" : "return a json about the sentiment information of an account (e.g. thread level, audience level)",
                
                '<twitter-handle>' :  "this is the twitter handle (Tweet ID) of the account you want to get information about"}
api.add_resource(index, '/')


# accounts endpoint
class accounts(Resource):
    def get(self):
        global accounts_names 
        global tweet_amount
        return {'accounts': accounts_names, 'tweet_amount': tweet_amount}
api.add_resource(accounts, '/accounts')



# tweets endpoint
class tweets(Resource):
    def get(self, twitter_handle):
        global tweet_amount

        df_conversation, _ = utils.search_tweets(tweet_amount, twitter_handle)

        
        return  df_conversation.drop(columns=["time", 'id', 'conversationId', 'inReplyToTweetId', 'pos', 'neg', 'neu']).to_dict(orient = 'records',)
    
api.add_resource(tweets, '/tweets/<twitter_handle>')


# audience endpoint
class audience(Resource):
    def get(self, twitter_handle):
        global tweet_amount

        df_conversation, accounts_names = utils.search_tweets(tweet_amount, twitter_handle)
        audience = df_conversation.username.unique().tolist()
        audience = [i for i in audience if i not in accounts_names]

        return {'audience': audience}
    
api.add_resource(audience, '/audience/<twitter_handle>')


# sentiment endpoint
class sentiment(Resource):
    def get(self, twitter_handle):
        global tweet_amount
        
        df_conversation, accounts_names= utils.search_tweets(tweet_amount, twitter_handle)
        
        dict_result = {}
        thread = df_conversation[df_conversation.username.isin([accounts_names])]
        dict_result['thread level'] = {'Positive': round(thread.pos.mean(),3), 
                                       'Negative': round(thread.neg.mean(),3), 
                                       'Neutral': round(thread.neu.mean(),3)}


        audience = df_conversation[~df_conversation.username.isin([accounts_names])]
        dict_result['audience level'] = {'Positive': round(audience.pos.mean(),3),
                                         'Negative': round(audience.neg.mean(),3),
                                         'Neutral': round(audience.neu.mean(),3)}
        
        return dict_result
    
api.add_resource(sentiment, '/sentiment/<twitter_handle>')



if __name__ == '__main__':
    app.run(debug=True)
