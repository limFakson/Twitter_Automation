from typing import Dict
from .types import ContentType

PROMPTS: Dict[ContentType, str] = {
    ContentType.UNITY_TIPS: """
    Write a concise Unity game development tip. 
    Start with phrases like "Did you know? 💡" or "Pro Tip:". 
    Focus on practical advice to improve workflow or game performance. 
    Keep the tip under 280 characters.  
    Only output the tweet text—nothing else.

    **Tweet Guidelines**:
    - Use trending hashtags from X (formerly Twitter) and one tech or game dev-related hashtag.
    - Avoid unnecessary context, intros, or explanations—only provide the tweet text.
    """.strip(),

    ContentType.GAME_DEV_THREAD: """
    Write a 3-4 tweet thread about a game dev concept or trend. 
    Topics: optimization, Unity best practices, or C# design patterns.
    Ensure the tweets flow logically and are each under 280 characters.  
    Only output the tweets—no extra explanations or intros.

    **Tweet Guidelines**:
    - Start with a bold statement, fact, or question to hook readers.
    - Use hashtags from X (formerly Twitter) sparingly but effectively.
    - Do not output anything other than the tweets.
    """.strip(),

    ContentType.GAME_NEWS: """
    Craft an engaging tweet about recent gaming trends, tools, or news. 
    Focus on Unity, indie games, or popular studios. 
    Keep it under 280 characters.  
    Only output the tweet—no explanations, preambles, or formatting instructions.

    **Tweet Guidelines**:
    - Use a hook like "Big news! 🚨" or "Gamers, take note! 🎮".
    - Include relevant hashtags from X (formerly Twitter).
    - Output only the tweet text, without any other context or explanation.
    """.strip(),

    ContentType.GAME_DEV_POLL: """
    Create an engaging poll about game development. 
    Example: "What's your go-to game engine? 💻" or "Which is harder: AI or optimization? 🤔". 
    Keep it under 280 characters.  
    Only output the poll text—no extra formatting or explanations.

    **Tweet Guidelines**:
    - Add a playful or humorous tone to increase engagement.
    - Include relevant hashtags from X (formerly Twitter).
    - Output only the poll text, without intros, preambles, or instructions.
    """.strip(),

    ContentType.GAME_DEV_MEME: """
    Write a funny, relatable tweet about game development struggles or joys. 
    Suggest a meme or GIF pairing if necessary. 
    Keep the tweet under 280 characters.  
    Only output the tweet text—no setup, explanation, or commentary.

    **Tweet Guidelines**:
    - Use humor and references that resonate with game devs.
    - Include trending hashtags from X (formerly Twitter) sparingly.
    - Output only the tweet text. No explanations, preambles, or formatting.
    """.strip(),

    ContentType.GAME_DEV_JOBS: """
    Write a tweet highlighting a recent game dev job posting. 
    Mention the role, company, and link to apply. 
    Keep it under 280 characters.  
    Only output the tweet text—no other context or explanations.

    **Tweet Guidelines**:
    - Use engaging phrases like "🚨 Hot job alert!" or "Looking for a new gig? 👾".
    - Include relevant hashtags from X (formerly Twitter).
    - Output only the tweet text, without any intros, preambles, or explanations.
    """.strip(),

    ContentType.GAME_NEWS_SOURCE: """
    Write an engaging tweet based on the given news source input. 
    Focus on gaming deals, updates, or trends. Keep the tweet under 280 characters.  
    Only output the tweet—do not include setup, explanation, or additional formatting.

    **Tweet Guidelines**:
    - For deals: Highlight the offer and include the link provided.
    - Use hooks like "Massive sale alert! 🛒" or "Big update! 🔥".
    - Include trending hashtags sparingly but effectively.
    - Output only the tweet text—no extra context, intros, or commentary.
    """.strip()
}



def get_prompt(content_type: ContentType) -> str:
    """Get the prompt template for a given content type"""
    return PROMPTS.get(content_type, "Generate a tweet about game development.")
