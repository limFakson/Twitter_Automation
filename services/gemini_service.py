import logging
import random
import google.generativeai as genai
from typing import Optional, List
from config.environment import load_environment
from content.types import MemeTemplate, Tweet, TweetType, ContentType, PollOption
from content.prompts import get_prompt

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        config = load_environment()
        genai.configure(api_key=config["GEMINI_API_KEY"])
        self.model = genai.GenerativeModel('gemini-1.5-pro')
    
    def generate_tweet(self, content_type: ContentType) -> Tweet:
        """Generate tweet content using Gemini AI"""
        try:
            prompt = get_prompt(content_type)
            response = self.model.generate_content(prompt)
            
            if content_type == ContentType.GAME_DEV_THREAD:
                return self._create_thread(f"{response.text}")
            elif content_type == ContentType.GAME_DEV_POLL:
                return self._create_poll(f"{response.text}")
            elif content_type == ContentType.GAME_DEV_MEME:
                return self._create_meme(f"{response.text}")
            else:
                return Tweet(
                    content=self._format_tweet(f"{response.text}"),
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
        tweets = [self._format_tweet(t) for t in text.split('\n\n') if t.strip()]
        return Tweet(
            content=text,
            tweet_type=TweetType.THREAD,
            thread_tweets=tweets
        )
    
    # Poll option is not working yet, twitter's api doesn't support polls yet
    def _create_poll(self, text: str) -> Tweet:
        """Create a poll from generated content"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if not lines:
            raise ValueError("No valid content generated for poll")
        
        question = lines[0]
        options = [
            PollOption(text=option)
            for option in lines[1:]
            if not option.startswith(('#', '?'))
        ][:4]  
        
        return Tweet(
            content=question,
            tweet_type=TweetType.POLL,
            poll_options=options
        )
    
    def _create_meme(self, text: str) -> Tweet:
        """Create a meme tweet with generated image"""
        try:
            template = random.choice(MemeTemplate.get_templates())
            
            image_path = self.meme_service.generate_meme(template, text)
            
            return Tweet(
                content=self._format_tweet(text),
                tweet_type=TweetType.MEME,
                image_path=image_path
            )
        except Exception as e:
            logger.error(f"Failed to create meme: {e}")
            return Tweet(
                content=self._format_tweet(text),
                tweet_type=TweetType.MEME
            )