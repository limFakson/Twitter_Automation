import logging
import time
import threading
from config.logging_config import setup_logging
from services.telegram_service import TelegramService

logger = logging.getLogger(__name__)


def main():
    setup_logging()
    start_time = time.time()
    run_duration = 60  # Run the script for 60 seconds

    try:
        telegram_service = TelegramService()
        # telegram_service.start()
        # print("Telegram service started")
        # while True:
        #     current_time = time.time()
        #     elapsed_time = current_time - start_time

        #     if elapsed_time > run_duration:
        #         logger.info(
        #             f"Time's up! {run_duration} seconds have passed. Stopping the script."
        #         )
        #         break

        #     # Add the logic you want to run in each loop iteration
        #     logger.info("Script is still running...")

        #     # Sleep for a short while to avoid 100% CPU usage
        #     time.sleep(5)  # Sleep for 5 seconds (You can adjust this)

    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise


if __name__ == "__main__":
    thread = threading(main(), daemon=True)
    thread.start()
