from enum import Enum
from dataclasses import dataclass
from typing import List, Optional

class ContentType(Enum):
    UNITY_TIPS = "unity_tips"
    GAME_DEV_THREAD = "game_dev_thread"
    GAME_NEWS = "game_news"
    GAME_DEV_POLL = "game_dev_poll"
    GAME_DEV_MEME = "game_dev_meme"
    GAME_DEV_JOBS = "game_dev_jobs"
    UNITY_TUTORIAL = "unity_tutorial"
    GAME_DESIGN = "game_design"
    INDIE_DEV = "indie_dev"
    GAME_MARKETING = "game_marketing"

class TweetType(Enum):
    NORMAL = "normal"
    THREAD = "thread"
    POLL = "poll"
    MEME = "meme"

@dataclass
class PollOption:
    text: str
    votes: int = 0

@dataclass
class Tweet:
    content: str
    tweet_type: TweetType
    image_path: Optional[str] = None
    poll_options: Optional[List[PollOption]] = None
    thread_tweets: Optional[List[str]] = None
    
    def format_preview(self) -> str:
        """Format tweet content for preview"""
        if self.tweet_type == TweetType.THREAD:
            return self._format_thread()
        elif self.tweet_type == TweetType.POLL:
            return self._format_poll()
        return self.content
    
    def _format_thread(self) -> str:
        if not self.thread_tweets:
            return self.content
        return "\n\n".join(f"🧵 {i}/{len(self.thread_tweets)} {tweet}"
                          for i, tweet in enumerate(self.thread_tweets, 1))
    
    def _format_poll(self) -> str:
        if not self.poll_options:
            return self.content
        options = "\n".join(f"{i}. {opt.text}"
                          for i, opt in enumerate(self.poll_options, 1))
        return f"{self.content}\n\nPoll Options:\n{options}"