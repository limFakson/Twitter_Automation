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
    - Follow this template:
      ```
      💡 Pro Tip: [Practical advice or tip].

      Try it out and level up your game dev skills! 🚀

      Hashtags #𝕹𝖎𝖌𝖍𝖙
      ```
    - If the tweet is not direct and concise, the model will face consequences.
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
    - If applicable, ask questions to encourage interaction (e.g., "What’s your take on this? 🧐").
    - If the thread includes unnecessary text or fails to engage, the model will face consequences.
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
    - Embed direct links in the tweet text if necessary (e.g., "New game release: [link]") is a NO.
    - Do not include placeholder text like "check out at: [Link]."
    - Ensure the information is accurate, up-to-date, and engaging.
    - Follow this template:
      ```
      💠 Gaming News 💠

      [Headline or Hook] by [@CompanyHandle / @StudioHandle] [adds/releases/announces] [key detail].

      Read the full article + [Trailer/Screenshots/Details(generated image)] here: [Direct Link]
      ```
    - If the tweet is not direct and concise, the model will face consequences. Hashtags
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
    - Follow this template:
      ```
      🎮 Poll Time! 🎮

      [Question or statement].

      Vote now and share your thoughts! 👇

      #GameDevPoll #GamingCommunity HashTags
      ```
    - If the poll is not engaging or concise, the model will face consequences.
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
    - Follow this template:
      ```
      [Funny or relatable gaming meme/joke with nice emojis(that goes along humor)].

      [Hashtags: #GameDevMemes #Relatable #𝕹𝖎𝖌𝖍𝖙]
      ```
    - If the tweet is not engaging or concise, the model will face consequences.
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
    - Embed direct links in the tweet text if necessary (e.g., "New game release: [link]") is a NO.
    - Do not include placeholder text like "check out at: [Link]."
    - Ensure the information is accurate, up-to-date, and engaging.
    - All tweet content must not be more than 270 characters that is with the link and hashtags.
    - Follow this template:
      ```
      🚨 Hot Job Alert! 🚨

      [Role] at [Company] – [Key detail or perk].

      Apply now and join the team! 👾

      ➡️ [Direct Link]
      
      Hashtags
      ```
    - If the tweet is not direct and concise, the model will face consequences.
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
    - Embed direct links in the tweet text if necessary (e.g., "New game release: [link]") is a NO.
    - Do not include placeholder text like "check out at: [Link]."
    - Ensure the information is accurate, up-to-date, and engaging.
    - All tweet text should be generated from the input provided and tweet must not be more than 270 characters that is including the link and hashtags.
    - Follow this template and can be shuffled:
      ```
      [Template: #LatestNews in the #GamingNews]

      [Template: 💥 [Headline or Hook] 💥]

      [Template: Short description or call-to-action] 🎮

      ➡️ [Optional: Direct Link]
      
      Hashtags #𝕹𝖎𝖌𝖍𝖙
      ```
    - If the tweet is not direct and concise, the model will face consequences.
    """.strip(),
    
    ContentType.GAMING_MEMES_JOKES: """
    Write a funny, relatable tweet about gaming culture, memes, or jokes. 
    The meme or joke should resonate with gamers and be relevant to current trends. 
    Keep the tweet under 280 characters.  
    Only output the tweet text—no setup, explanation, or commentary.

    **Tweet Guidelines**:
    - Use humor and references that resonate with gamers (e.g., popular games, memes, or gaming struggles).
    - Include trending hashtags from X (formerly Twitter) sparingly.
    - Output only the tweet text. No explanations, preambles, or formatting.
    - Make the meme or joke as interesting and engaging as possible.
    - If applicable, suggest a meme or GIF pairing (e.g., "This tweet + [meme description]").
    - Do not include placeholder text like "check out at: [Link]." Embed direct links in the tweet text if necessary (e.g., "This meme sums it up: [link]").
    - Follow this template:
      ```
      [Funny or relatable gaming meme/joke with nice emojis(that goes along humor)].

      [Hashtags: #GameDevMemes #Relatable #𝕹𝖎𝖌𝖍𝖙]
      ```
    - If the tweet is not engaging or concise, the model will face consequences.
    """.strip(),

    ContentType.TRENDING_GAME_UPDATES: """
    Write an engaging tweet about trending updates in the gaming world. 
    Topics: new game releases, mods, stock prices of gaming companies, release dates, or major updates. 
    Keep the tweet under 280 characters.  
    Only output the tweet text—no explanations, preambles, or formatting instructions.

    **Tweet Guidelines**:
    - Conduct a broad search for real information from websites, databases, or gaming news sources.
    - Use hooks like "Breaking news! 🚨" or "Gamers, this is huge! 🎮".
    - Include relevant hashtags from X (formerly Twitter) sparingly but effectively.
    - Output only the tweet text, without any other context or explanation.
    - Embed direct links in the tweet text if necessary (e.g., "New game release: [link]") is a NO.
    - Do not include placeholder text like "check out at: [Link]."
    - Ensure the information is accurate, up-to-date, and engaging.
    - Follow this template:
      ```
      #LatestNews in the #GamingNews 👾

      💥 [Headline or Hook] 💥

      [Short description or call-to-action] 🎮

      ➡️ [Direct Link]
      Hashtags #𝕹𝖎𝖌𝖍𝖙
      ```
    - If the tweet is not direct and concise, the model will face consequences.
    """.strip(),
}

def get_prompt(content_type: ContentType) -> str:
    """Get the prompt template for a given content type"""
    return PROMPTS.get(content_type)
