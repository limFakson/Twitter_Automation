from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

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
        formatters = {
            TweetType.THREAD: self._format_thread,
            TweetType.POLL: self._format_poll,
            TweetType.MEME: self._format_meme,
            TweetType.NORMAL: lambda: self.content
        }
        return formatters[self.tweet_type]()
    
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
    
    def _format_meme(self) -> str:
        return f"{self.content}" # Image will be handled separately