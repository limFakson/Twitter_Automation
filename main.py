import logging
import time
import threading
from config.logging_config import setup_logging
from services.telegram_service import TelegramService
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.background import BackgroundScheduler
from services.news_service import NewsService

logger = logging.getLogger(__name__)
scheduler = BackgroundScheduler()

def news_service_job():
    logger.info("Running news service job...")
    news_service = NewsService()    
    news_feed = news_service.games_news()
    return news_feed

def jobstore():
    # Run every day at 8 AM and 7 PM
    scheduler.add_job(
        news_service_job,
        trigger=CronTrigger(hour="8,19", minute=0)
    )
    scheduler.start()
    logger.info("Scheduler started with jobs.")


def main():
    try:
        # Start your job store
        jobstore()

        telegram_service = TelegramService()
        # telegram_service.start()

        logger.info("Main service started.")

        # Keep process alive
        while True:
            logger.info("Script is still running...")
            time.sleep(5)

    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise


if __name__ == "__main__":
    # ✅ Correct threading usage
    thread = threading.Thread(target=main, daemon=True)
    thread.start()

    # Keep main thread alive
    while True:
        time.sleep(1)
