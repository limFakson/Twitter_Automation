import logging
import random
from typing import Optional
from utils.types import Tweet, TweetType, ContentType, PollOption
from utils.prompts import get_prompt
from services.gemini_service import GeminiService

logger = logging.getLogger(__name__)

class ContentService:
    def __init__(self):
        self.gemini = GeminiService()
    
    def generate_tweet(self) -> Tweet:
        """Generate a new tweet using Gemini AI"""
        try:
            content_type = random.choice(list(ContentType))
            if content_type == "ContentType.GAME_NEWS_SOURCE":
                self.generate_tweet()
            print(content_type)
            return self.gemini.generate_tweet(content_type)
        except Exception as e:
            logger.error(f"Failed to generate tweet: {e}")
            raise
    
    def generate_tweet_news(self, input) -> Tweet:
        """"Generate news tweet from ign news"""
        try:
            content_type = ContentType.GAME_NEWS_SOURCE
            return self.gemini.generate_tweet_news(content_type, input)
        except Exception as e:
            logger.error(f"Failed to generate tweet: {e}")
            raise
    
    def update_tweet(self, original_tweet: Tweet, new_content: str, edit_type: str) -> Tweet:
        """Update an existing tweet with new content"""
        try:
            if edit_type == 'edit_thread':
                return self._update_thread(original_tweet, new_content)
            elif edit_type == 'edit_poll':
                return self._update_poll(original_tweet, new_content)
            else:
                return Tweet(
                    content=new_content,
                    tweet_type=original_tweet.tweet_type,
                    image_path=original_tweet.image_path
                )
        except Exception as e:
            logger.error(f"Failed to update tweet: {e}")
            raise
    
    def _update_thread(self, original_tweet: Tweet, new_content: str) -> Tweet:
        """Update a thread tweet"""
        return Tweet(
            content=new_content,
            tweet_type=TweetType.THREAD,
            thread_tweets=new_content.split('\n\n')
        )
    
    def _update_poll(self, original_tweet: Tweet, new_content: str) -> Tweet:
        """Update a poll tweet"""
        lines = new_content.split('\n')
        question = lines[0]
        options = [PollOption(text=line.strip()) for line in lines[1:] if line.strip()]
        
        return Tweet(
            content=question,
            tweet_type=TweetType.POLL,
            poll_options=options
        )