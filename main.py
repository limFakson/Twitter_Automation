import logging
from config.logging_config import setup_logging
from services.telegram_service import TelegramService

logger = logging.getLogger(__name__)

def main():
    setup_logging()
    
    try:
        telegram_service = TelegramService()
        telegram_service.start()
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise

if __name__ == "__main__":
    main()