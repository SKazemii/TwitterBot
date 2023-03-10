import schedule
import time
import utils

def job():
    '''Runs the job every 24 hours'''
    # # Saving the last 10000 Elon's tweets
    # utils.search_tweets('elonmusk', 10000)
    # utils.logger.info("Elon Done!")

    # # Saving the last 10000 Barack's tweets
    # utils.search_tweets('BarackObama', 10000)
    # utils.logger.info("Barack Done!")

    # Saving the last 10000 Taylor's tweets
    utils.search_tweets('binsideoutb', 300)
    utils.logger.info("ylecun Done!")

    utils.logger.info("Done!")


if __name__ == "__main__":
    utils.logger.info("Running Scraper")
    # Schedule the job to run every 24 hours at midnight
    job()
    schedule.every().day.at("00:00").do(job)

    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
    
    