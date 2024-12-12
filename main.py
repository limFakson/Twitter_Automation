import logging
from config.logging_config import setup_logging
from services.telegram_service import TelegramService
from services.twitter_service import TwitterService
from services.gemini_service import GeminiService

def main():
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Initialize services
        telegram = TelegramService()
        twitter = TwitterService()
        gemini = GeminiService()
        
        # Start bot
        telegram.start()
        logger.info("Bot started successfully")
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise

if __name__ == "__main__":
    main()