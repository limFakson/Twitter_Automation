import tweepy
import logging
import requests
import os
from typing import Optional
from config.environment import load_environment
from utils.types import Tweet, TweetType

import time
from requests_oauthlib import OAuth1

logger = logging.getLogger(__name__)

class TwitterService:
    def __init__(self):
        self.config = load_environment()
        self._setup_clients()
        # Twitter API endpoints
        self.MEDIA_ENDPOINT_URL = 'https://upload.twitter.com/1.1/media/upload.json'
    
    def _setup_clients(self):
        """Initialize Twitter API clients"""
        # v2 client for posting tweets (still works fine)
        self.client = tweepy.Client(
            consumer_key=self.config["TWITTER_API_KEY"],
            consumer_secret=self.config["TWITTER_API_SECRET"],
            access_token=self.config["TWITTER_ACCESS_TOKEN"],
            access_token_secret=self.config["TWITTER_ACCESS_SECRET"]
        )
        
        # OAuth1 auth for manual media upload (replacing tweepy.API)
        self.auth = OAuth1(
            self.config["TWITTER_API_KEY"],
            self.config["TWITTER_API_SECRET"],
            self.config["TWITTER_ACCESS_TOKEN"],
            self.config["TWITTER_ACCESS_SECRET"]
        )
    
    def post_tweet(self, tweet: Tweet) -> bool:
        """Post tweet based on its type"""
        try:
            if tweet.tweet_type == TweetType.THREAD:
                return self._post_thread(tweet)
            # elif tweet.tweet_type == TweetType.POLL:
            #     return self._post_poll(tweet)
            else:
                return self._post_single(tweet)
        except Exception as e:
            logger.error(f"Failed to post tweet: {e}")
            return False
            
    def _upload_media_chunked(self, file_path, media_type="image/jpeg"):
        """
        Manually upload media using the Chunked Upload flow (INIT -> APPEND -> FINALIZE).
        This bypasses tweepy.API.media_upload which is deprecated/broken for V2-only apps.
        """
        try:
            total_bytes = os.path.getsize(file_path)
            logger.info(f"Starting chunked upload for {file_path} ({total_bytes} bytes)")

            # STEP 1: INIT
            init_data = {
                'command': 'INIT',
                'media_type': media_type,
                'total_bytes': total_bytes,
                'media_category': 'tweet_image'
            }
            init_req = requests.post(url=self.MEDIA_ENDPOINT_URL, data=init_data, auth=self.auth)
            
            if init_req.status_code > 299:
                logger.error(f"Error INIT media upload: {init_req.text}")
                return None
            
            media_id = init_req.json()['media_id_string']
            logger.debug(f"Media ID Init: {media_id}")

            # STEP 2: APPEND
            segment_id = 0
            bytes_sent = 0
            with open(file_path, 'rb') as f:
                while bytes_sent < total_bytes:
                    chunk = f.read(4 * 1024 * 1024) # 4MB chunks
                    
                    req_data = {
                        'command': 'APPEND',
                        'media_id': media_id,
                        'segment_index': segment_id
                    }
                    files = {
                        'media': chunk
                    }
                    append_req = requests.post(url=self.MEDIA_ENDPOINT_URL, data=req_data, files=files, auth=self.auth)
                    
                    if append_req.status_code > 299:
                        logger.error(f"Error APPEND media upload: {append_req.text}")
                        return None
                    
                    segment_id += 1
                    bytes_sent = f.tell()

            # STEP 3: FINALIZE
            finalize_data = {
                'command': 'FINALIZE',
                'media_id': media_id
            }
            finalize_req = requests.post(url=self.MEDIA_ENDPOINT_URL, data=finalize_data, auth=self.auth)
            
            if finalize_req.status_code > 299:
                logger.error(f"Error FINALIZE media upload: {finalize_req.text}")
                return None
            
            finalize_resp = finalize_req.json()
            
            if 'processing_info' in finalize_resp:
                self._check_status(media_id, finalize_resp['processing_info'])
                
            logger.info(f"Media uploaded successfully: {media_id}")
            return media_id

        except Exception as e:
            logger.error(f"Exception during media upload: {e}")
            return None

    def _check_status(self, media_id, processing_info):
        """Check the processing status of the uploaded media"""
        if processing_info['state'] == 'succeeded':
            return

        interval = processing_info.get('check_after_secs', 1)
        time.sleep(interval)

        status_req = requests.get(
            url=self.MEDIA_ENDPOINT_URL, 
            params={'command': 'STATUS', 'media_id': media_id}, 
            auth=self.auth
        )
        
        processing_info = status_req.json().get('processing_info', {})
        if processing_info['state'] == 'succeeded':
            return
        elif processing_info['state'] == 'failed':
             raise Exception("Media processing failed")
        else:
            self._check_status(media_id, processing_info)
    
    def _post_single(self, tweet: Tweet) -> bool:
        """Post a single tweet with optional media"""
        try:
            media_ids = []
            if tweet.image_path:
                media_id = self._upload_media_chunked(tweet.image_path)
                if media_id:
                    media_ids.append(media_id)
            elif tweet.image_url:
                image_loc = "temp_image.jpg" # image path
                # download the image from url
                try:
                    response = requests.get(tweet.image_url, stream=True)
                    response.raise_for_status()
                    with open(image_loc, "wb") as f:
                        f.write(response.content)
                    
                    # upload downloaded image
                    media_id = self._upload_media_chunked(image_loc)
                    if media_id:
                        media_ids.append(media_id)
                except Exception as e:
                    logger.error(f"Failed to download/upload image from URL: {e}")
                
            
            # Wait for media to be processed by Twitter before posting
            if media_ids:
                logger.info("Waiting 5 seconds for media processing...")
                time.sleep(5)
            
            # Retry logic for 503 Service Unavailable
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    self.client.create_tweet(
                        text=tweet.content,
                        media_ids=media_ids if media_ids else None
                    )
                    return True
                except Exception as e:
                    if "503" in str(e) and attempt < max_retries - 1:
                        wait_time = (attempt + 1) * 5
                        logger.warning(f"503 Service Unavailable. Retrying in {wait_time}s (Attempt {attempt + 1}/{max_retries})...")
                        time.sleep(wait_time)
                    else:
                        logger.error(f"Error posting single tweet: {e}")
                        return False
            
            return False
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

    def search_hashtags(self, keyword: str) -> list:
        """Search for relevant hashtags based on a keyword using recent tweets"""
        try:
            logger.info(f"Searching for hashtags related to: {keyword}")
            # Search for recent tweets containing the keyword
            response = self.client.search_recent_tweets(
                query=f"{keyword} -is:retweet lang:en",
                max_results=20,
                tweet_fields=['entities']
            )
            
            if not response.data:
                return []
            
            hashtags = {}
            for tweet in response.data:
                if tweet.entities and 'hashtags' in tweet.entities:
                    for tag in tweet.entities['hashtags']:
                        t = f"#{tag['tag']}"
                        hashtags[t] = hashtags.get(t, 0) + 1
            
            # Sort by frequency
            sorted_tags = sorted(hashtags.items(), key=lambda x: x[1], reverse=True)
            return [tag[0] for tag in sorted_tags[:10]] # Return top 10
            
        except Exception as e:
            logger.error(f"Failed to search hashtags: {e}")
            return []