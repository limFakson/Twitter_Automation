from dotenv import load_dotenv
import os
import logging

logger = logging.getLogger(__name__)

REQUIRED_VARS = [
    "TWITTER_API_KEY",
    "TWITTER_API_SECRET", 
    "TWITTER_ACCESS_TOKEN",
    "TWITTER_ACCESS_SECRET",
    "TELEGRAM_BOT_TOKEN",
    "TELEGRAM_CHAT_ID",
    "GEMINI_API_KEY",
    # "CHECKER_BOT_TOKEN",
    "CHATGPT_4_API_KEY"
]

def load_environment():
    """Load and validate environment variables"""
    load_dotenv()
    
    config = {}
    for var in REQUIRED_VARS:
        value = os.getenv(var)
        if not value:
            raise ValueError(f"Missing required environment variable: {var}")
        config[var] = value
    
    return config