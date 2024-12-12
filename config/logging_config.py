import logging
import os
from datetime import datetime

def setup_logging():
    """Configure application logging"""
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Generate log filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d')
    log_file = f'logs/bot_{timestamp}.log'
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    # Create logger
    logger = logging.getLogger(__name__)
    logger.info('Logging configured successfully')