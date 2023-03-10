import schedule
import time
import utils




def job():
    api = utils.tweeter_API()
    # tweets_dict = utils.get_tweets(username, tweet_amount)
    tweets_dict = utils.get_tweets_from_file('/home/htl/Desktop/TwitterBot/Data/data2.json')
    Data_frame = utils.get_tweets_dataframe(tweets_dict)
    utils.save_data(Data_frame)

    utils.logger.info("Done!")





if __name__ == "__main__":
    utils.logger.info("running main.py")
    job()
    # Schedule the job to run every 24 hours at midnight
    # schedule.every().day.at("00:00").do(job)
    schedule.every().minute.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)
    