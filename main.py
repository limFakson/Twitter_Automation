import logging
import time
import threading
from config.logging_config import setup_logging
from services.telegram_service import TelegramService
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.background import BackgroundScheduler
from services.news_service import NewsService
import pytz
import random

setup_logging()
logger = logging.getLogger(__name__)
scheduler = BackgroundScheduler()

telegram_service = TelegramService()

def news_service_job(automate:bool=None):
    logger.info("Running news service job...")
    news_service = NewsService()    
    if not automate:
        news_feed = news_service.games_news()
        telegram_service._send_news(news_feed)
        return "Manual tweet"
    
    # Automated news post
    limit = random.randint(0,5)
    news_feed = news_service.games_news(limit)
    for news in news_feed:
        tweet = telegram_service.content_service.generate_tweet_news(news)
        success = telegram_service.twitter.post_tweet(tweet)
        if success:
            logger.info(f'News post tweeted on X - {time.asctime()}')
    return "Automated Tweet"

def jobstore():
    # Run every day at 8 AM and 7 PM
    scheduler.add_job(
        news_service_job,
        trigger=CronTrigger(hour="17", minute=0, timezone=pytz.timezone("UTC")),
        id="news service"
    )
    scheduler.add_job(
        news_service_job,
        trigger=CronTrigger(hour="9,14", minute=13, timezone=pytz.timezone("UTC")),
        args=[True],
        id="automated news service"
    )
    scheduler.start()
    logger.info("Scheduler started with jobs.")


def main():
    try:
        # Start your job store
        jobstore()

        logger.info("Main service started.")
        # Keeps process alive
        telegram_service.start_bot()
            
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise
    finally:
        telegram_service.stop()


if __name__ == "__main__":
    # Keep main thread alive
    main()
