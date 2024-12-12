from enum import Enum
from typing import Dict

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

PROMPTS: Dict[ContentType, str] = {
    ContentType.UNITY_TIPS: """
    Generate a helpful Unity game development tip in a tweet format.
    Focus on practical, specific advice that can improve development workflow or game performance.
    Keep it under 280 characters.
    """.strip(),
    
    ContentType.GAME_DEV_THREAD: """
    Create a thread of 3-4 tweets about game development.
    Each tweet should be under 280 characters.
    Focus on: optimization, design patterns, or Unity best practices.
    Format as a thread with clear connections between tweets.
    """.strip(),
    
    # Add other prompts similarly...
}

def get_prompt(content_type: ContentType) -> str:
    """Get the prompt template for a given content type"""
    return PROMPTS.get(content_type, "Generate a tweet about game development.")