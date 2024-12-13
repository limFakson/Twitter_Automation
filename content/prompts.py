from typing import Dict
from .types import ContentType

PROMPTS: Dict[ContentType, str] = {
    ContentType.UNITY_TIPS: """
    Generate a helpful Unity game development tip in a tweet format.
    Focus on practical, specific advice that can improve development workflow or game performance.
    Keep it under 280 characters.
    Include relevant hashtags like #UnityTips #GameDev
    """.strip(),
    
    ContentType.GAME_DEV_THREAD: """
    Create a thread of 3-4 tweets about an important game development concept.
    Each tweet should be under 280 characters.
    Focus on one of these areas: optimization, design patterns, or Unity best practices.
    Make sure tweets are connected logically and flow well together.
    Include relevant hashtags like #GameDev #UnityTips
    """.strip(),
    
    ContentType.GAME_NEWS: """
    Generate a tweet about a recent trend or innovation in game development.
    Focus on Unity, indie games, or game development tools.
    Keep it informative and under 280 characters.
    Include relevant hashtags like #GameDev #UnityNews
    """.strip(),
    
    ContentType.GAME_DEV_POLL: """
    Create an engaging poll about game development preferences or practices.
    Format: One question followed by 2-4 options.
    Make it relevant to Unity developers and indie game creators.
    Keep the question under 280 characters.
    Include relevant hashtags like #GameDev #UnityPoll
    """.strip(),
    
    ContentType.GAME_DEV_MEME: """
    Generate a humorous tweet about a common game development experience or challenge.
    Make it relatable to Unity developers and indie game creators.
    Keep it light and under 280 characters.
    Include relevant hashtags like #GameDev #UnityMemes
    """.strip(),
    
    ContentType.GAME_DEV_JOBS: """
    Create a tweet highlighting key skills or roles in high demand in game development.
    Focus on Unity development and indie game creation.
    Keep it informative and under 280 characters.
    Include relevant hashtags like #GameDevJobs #UnityJobs
    """.strip()
}

def get_prompt(content_type: ContentType) -> str:
    """Get the prompt template for a given content type"""
    return PROMPTS.get(content_type, "Generate a tweet about game development.")