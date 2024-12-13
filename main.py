import logging
from config.logging_config import setup_logging
from services.telegram_service import TelegramService

logger = logging.getLogger(__name__)

def main():
    # Setup logging
    setup_logging()
    
    try:
        # Initialize and start telegram service
        telegram_service = TelegramService()
        telegram_service.start()
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise

if __name__ == "__main__":
    main()