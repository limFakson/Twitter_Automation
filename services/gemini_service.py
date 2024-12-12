import google.generativeai as genai
import logging
import os
from typing import Optional
from config.environment import load_environment
from content.prompts import ContentType, get_prompt
from content.types import Tweet, TweetType

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        config = load_environment()
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def generate_tweet(self, content_type: ContentType) -> Tweet:
        """Generate tweet content using Gemini AI"""
        try:
            prompt = get_prompt(content_type)
            response = self.model.generate_content(prompt)
            
            if content_type == ContentType.GAME_DEV_THREAD:
                return self._create_thread(response.text)
            elif content_type == ContentType.GAME_DEV_POLL:
                return self._create_poll(response.text)
            elif content_type == ContentType.GAME_DEV_MEME:
                return self._create_meme(response.text)
            else:
                return Tweet(
                    content=self._format_tweet(response.text),
                    tweet_type=TweetType.NORMAL
                )
        except Exception as e:
            logger.error(f"Gemini content generation failed: {e}")
            raise
    
    def _format_tweet(self, text: str) -> str:
        """Format text to meet Twitter's character limit"""
        return text[:277] + "..." if len(text) > 280 else text
    
    def _create_thread(self, text: str) -> Tweet:
        """Create a thread from generated content"""
        tweets = [self._format_tweet(t) for t in text.split('\n\n')]
        return Tweet(
            content=text,
            tweet_type=TweetType.THREAD,
            thread_tweets=tweets
        )
    
    def _create_poll(self, text: str) -> Tweet:
        """Create a poll from generated content"""
        # Implementation for poll creation
        pass
    
    def _create_meme(self, text: str) -> Tweet:
        """Create a meme tweet with image"""
        # Implementation for meme creation
        pass