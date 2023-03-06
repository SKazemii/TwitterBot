from flask import Flask
from flask_restful import Resource, Api

import utils


app = Flask(__name__)
api = Api(app)




# accounts endpoint
class accounts(Resource):
    def get(self):
        dataframe = utils.load_data()
        users = dataframe['user'].unique().tolist()
        return {'accounts': users}
api.add_resource(accounts, '/accounts')


# tweets endpoint
class tweets(Resource):
    def get(self, twitter_handle):
        return {'tweets': twitter_handle}
api.add_resource(tweets, '/tweets/<twitter_handle>')


# audience endpoint
class audience(Resource):
    def get(self, twitter_handle):
        return {'audience': twitter_handle}
api.add_resource(audience, '/audience/<twitter_handle>')


# sentiment endpoint
class sentiment(Resource):
    def get(self, twitter_handle):
        return {'sentiment': twitter_handle}
api.add_resource(sentiment, '/sentiment/<twitter_handle>')



if __name__ == '__main__':
    dataframe = utils.load_data()
    users = dataframe['user'].unique()
    print({'accounts': users})
    app.run(debug=True)