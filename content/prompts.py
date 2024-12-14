from typing import Dict
from .types import ContentType

PROMPTS: Dict[ContentType, str] = {
    ContentType.UNITY_TIPS: """
    Generate quick tips on game development using Unity Starting with something like "Did you know? 💡..." or "Pro Tip:" on the first line, then the tip on the next line. 
    Focus on practical, specific advice that can improve development workflow or game performance.
    Keep it under 280 characters.
    Search the web and include relevant currently trending hashtags in x(formerly known as twitter) and also add an hashtag that hints on tech or game dev
    """.strip(),
    
    ContentType.GAME_DEV_THREAD: """
    Create a thread of 3-4 tweets about an important game development concept or a trend on tips in game development.
    Each tweet should be under 280 characters.
    Focus on one of these areas: optimization, design patterns, or Unity best practices, coding in c# and more e.t.c (search the web for content).
    Make sure tweets are connected logically and flow well together.
    Search the web and include relevant currently trending hashtags in x(formerly known as twitter) and also add an hashtag that hints on tech or game dev
    """.strip(),
    
    ContentType.GAME_NEWS: """
    Generate a tweet about a recent trend or innovation in games, gamer news, games update, game industry, gamers, .
    Focus on Unity, indie games, popular game companies, game industry, or game development tools.
    Keep it informative, creative, fun and under 280 characters.
    Search the web and include relevant currently trending hashtags in x(formerly known as twitter) and also add an hashtag that hints on tech or game dev
    """.strip(),
    
    ContentType.GAME_DEV_POLL: """
    Create an engaging poll about game development preferences or practices.
    Format: One question followed by 2-4 options.
    Make it relevant to Unity developers and indie game creators.
    Keep the question under 280 characters.
    Search the web and include relevant currently trending hashtags in x(formerly known as twitter) and also add an hashtag that hints on tech or game dev
    """.strip(),
    
    ContentType.GAME_DEV_MEME: """
    Generate a humorous tweet about a common game development experience or challenge find a matching image and add it.
    Make it relatable to Game developers and indie game creators.
    Keep it light and under 280 characters.
    Search the web and include relevant currently trending hashtags in x(formerly known as twitter) and also add an hashtag that hints on tech or game dev
    """.strip(),
    
    ContentType.GAME_DEV_JOBS: """
    Search the web for actively open job posting on game dev (max job post day (3 days ago)) 
    Create a tweet highlighting lists of available jobs found from web search and links to apply to them
    Focus on all game development job roles (programmers, artists, designers, etc.)
    Keep it informative and under 280 characters.
    Search the web and include relevant currently trending hashtags in x(formerly known as twitter) and also add an hashtag that hints on tech or game dev
    """.strip()
}

def get_prompt(content_type: ContentType) -> str:
    """Get the prompt template for a given content type"""
    return PROMPTS.get(content_type, "Generate a tweet about game development.")