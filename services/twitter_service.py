import tweepy
import logging
import requests
import os
from typing import Optional
from config.environment import load_environment
from utils.types import Tweet, TweetType

logger = logging.getLogger(__name__)

class TwitterService:
    def __init__(self):
        self.config = load_environment()
        self._setup_clients()
    
    def _setup_clients(self):
        """Initialize Twitter API clients"""
        # v2 client for modern endpoints
        self.client = tweepy.Client(
            consumer_key=self.config["TWITTER_API_KEY"],
            consumer_secret=self.config["TWITTER_API_SECRET"],
            access_token=self.config["TWITTER_ACCESS_TOKEN"],
            access_token_secret=self.config["TWITTER_ACCESS_SECRET"]
        )
        
        # v1.1 client for media upload
        auth = tweepy.OAuthHandler(
            self.config["TWITTER_API_KEY"],
            self.config["TWITTER_API_SECRET"]
        )
        auth.set_access_token(
            self.config["TWITTER_ACCESS_TOKEN"],
            self.config["TWITTER_ACCESS_SECRET"]
        )
        self.api = tweepy.API(auth)
    
    def post_tweet(self, tweet: Tweet) -> bool:
        """Post tweet based on its type"""
        try:
            if tweet.tweet_type == TweetType.THREAD:
                return self._post_thread(tweet)
            elif tweet.tweet_type == TweetType.POLL:
                return self._post_poll(tweet)
            else:
                return self._post_single(tweet)
        except Exception as e:
            logger.error(f"Failed to post tweet: {e}")
            return False
    
    def _post_single(self, tweet: Tweet) -> bool:
        """Post a single tweet with optional media"""
        try:
            media_ids = []
            if tweet.image_path:
                media = self.api.media_upload(tweet.image_path)
                media_ids.append(media.media_id)
            elif tweet.image_url:
                image_loc = "temp_image.jpg" # image path
                # download the image from url
                response = requests.get(tweet.image_url, stream=True)
                with open(image_loc, "wb") as f:
                    f.write(response.content)
                
                # upload downloaded image
                media = self.api.media_upload(image_loc)
                media_ids.append(media.media_id)
                
            
            self.client.create_tweet(
                text=tweet.content,
                media_ids=media_ids if media_ids else None
            )
            
            
            return True
        except Exception as e:
            logger.error(f"Error posting single tweet: {e}")
            return False
    
    def _post_thread(self, tweet: Tweet) -> bool:
        """Post a thread of tweets"""
        try:
            previous_id = None
            for content in tweet.thread_tweets:
                response = self.client.create_tweet(
                    text=content,
                    in_reply_to_tweet_id=previous_id
                )
                previous_id = response.data['id']
            return True
        except Exception as e:
            logger.error(f"Error posting thread: {e}")
            return False
    
    def _post_poll(self, tweet: Tweet) -> bool:
        """Post a poll tweet"""
        # Implementation for poll posting until when API supports it
        logger.warning("Poll posting not yet implemented")
        return self._post_single(tweet)