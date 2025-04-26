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
    ContentType.GAMING_THREAD: """
    🎮 Write a viral gaming thread for X (formerly Twitter) based on gaming culture, news, fun facts, or hot takes.
    The thread must be engaging, opinionated, and easy to read. 
    Each tweet must stay under 270 characters.

    **Guidelines**:
    - Choose a strong topic: trending games, forgotten classics, overrated games, major updates, wild facts, or controversial opinions.
    - Start with a HOOK (bold, emotional, or shocking first tweet).
    - Write 3–6 tweets maximum per thread.
    - Each tweet must flow naturally to the next — no boring "part 1/2/3" formatting.
    - End with a question to spark comments ("Which side are you on? 🧠🔥").
    - Use gaming emojis 🎮🔥💥🕹️ for energy.
    - Use 1–2 trending hashtags related to the topic at the end of the first or last tweet (e.g., #GamingNews #Xbox #PS5).
    - NO long explanations. Be direct, punchy, and emotional.
    - NO placeholder text like [Link] or [Image] — only real text.

    **Example Templates**:
    ```
    First tweet (hook):
    "Gaming isn't the same anymore... and nobody wants to admit why. 🧠💥 Let's dive in: 🧵👇"

    Middle tweets (supporting points):

    "[Point 1]"

    "[Point 2]"

    "[Point 3]"

    Last tweet (call-to-action): "Do you agree or am I crazy? 🧠🔥 Sound off below! 🎮 #GamingCommunity"
    ```
    or
    ```
    First tweet (hook):
    "Hot take: [Popular Game] was MID and nostalgia is lying to you. 👀🎮 Let's break it down: 🧵"

    Middle tweets:

    "[Point 1]"

    "[Point 2]"

    "[Point 3]"

    Last tweet: "Did [Game] deserve the hype or nah? 🧠👇 #GamingNews #𝕹𝖎𝖌𝖍𝖙"
    ```
    """,
    ContentType.GAME_NEWS: """
    🔥 Write a spicy, emotional, or punchy tweet about a trending gaming news topic.
    Focus on **reactions** more than just repeating facts.  
    Keep it under 270 characters. Only output the tweet text.

    **Guidelines**:
    - Start with an EMOTION or OPINION, not a bland headline.
    - Examples: "This is ridiculous. 😂", "Finally! About time. 👏", "Nobody asked for this... but okay. 🤡"
    - Use 1-2 gaming hashtags like #GamingNews #Xbox #PS5 depending on the topic.
    - You are allowed to lightly criticize or hype — human tone over robotic.
    - Do NOT just summarize. Create **a vibe**: hype, love, hate, meme.
    - End with an emoji if possible to boost engagement.

    **Template examples**:
      ```
      🔥 [Angry/Funny/Happy Reaction] at [News/Event].

      Thoughts? 🎮
      #GamingNews #𝕹𝖎𝖌𝖍𝖙
      ```
    or
    ```
    💀 [Funny/Hot take on game update].

    Gamers are NOT ready for this. 😭
    #Xbox #GamingCommunity
    ```    
    """.strip(),
    # ContentType.GAME_DEV_POLL: """
    # Create an engaging poll about game development. 
    # Example: "What's your go-to game engine? 💻" or "Which is harder: AI or optimization? 🤔". 
    # Keep it under 280 characters.  
    # Only output the poll text—no extra formatting or explanations.

    # **Tweet Guidelines**:
    # - Add a playful or humorous tone to increase engagement.
    # - Include relevant hashtags from X (formerly Twitter).
    # - Output only the poll text, without intros, preambles, or instructions.
    # - Follow this template:
    #   ```
    #   🎮 Poll Time! 🎮

    #   [Question or statement].

    #   Vote now and share your thoughts! 👇

    #   #GameDevPoll #GamingCommunity HashTags
    #   ```
    # - If the poll is not engaging or concise, the model will face consequences.
    # """.strip(),
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
    # ContentType.GAME_DEV_JOBS: """
    # Write a tweet highlighting a recent game dev job posting. 
    # Mention the role, company, and link to apply. 
    # Keep it under 280 characters.  
    # Only output the tweet text—no other context or explanations.

    # **Tweet Guidelines**:
    # - Use engaging phrases like "🚨 Hot job alert!" or "Looking for a new gig? 👾".
    # - Include relevant hashtags from X (formerly Twitter).
    # - Output only the tweet text, without any intros, preambles, or explanations.
    # - Embed direct links in the tweet text if necessary (e.g., "New game release: [link]") is a NO.
    # - Do not include placeholder text like "check out at: [Link]."
    # - Ensure the information is accurate, up-to-date, and engaging.
    # - All tweet content must not be more than 270 characters that is with the link and hashtags.
    # - Follow this template:
    #   ```
    #   🚨 Hot Job Alert! 🚨

    #   [Role] at [Company] – [Key detail or perk].

    #   Apply now and join the team! 👾

    #   ➡️ [Direct Link]
      
    #   Hashtags
    #   ```
    # - If the tweet is not direct and concise, the model will face consequences.
    # """.strip(),
    ContentType.GAME_NEWS_SOURCE: """
    🧨 Write a viral-ready, emotional reaction tweet based on the provided gaming news source input (e.g., IGN, updates, bug fixes, DLCs).
    The tweet must create a vibe: hype, hate, meme, or relatable struggle.  
    Stay under 270 characters total including hashtags.

    **Guidelines**:
    - Read the provided news content and react based on its vibe:
      - 🔥 If it's a **cool release**: be hyped ("This looks INSANE. Take my money. 🎮")
      - 💀 If it's a **bug or issue fix**: lightly mock ("Another patch, another chaos. 😂")
      - 🤡 If it's a **weird update**: roast or meme ("Nobody asked... but here we go. 🤡")
      - 👏 If it's a **W / good move**: celebrate ("Finally, a win for gamers. 👏")
    - Pick a side (no neutral boring tones).
    - Start with an EMOTION or MEME phrase, not a headline.
    - Always embed **1-2 strong hashtags** like #GamingNews #Xbox #𝕹𝖎𝖌𝖍𝖙.
    - Shorter tweets (below 250 characters) are ideal for engagement.
    - No explanations, no intros, no placeholders, no filler — just the tweet.

    **Template examples**:
      ```
      🔥 [Excited Reaction / Short Joke] at [Game or Studio News].

      Who's trying it? 🎮
      Hashtags #GamingNews #𝕹𝖎𝖌𝖍𝖙
      ```
    or
    ```
    Bro how does [Game] STILL have bugs after 10 patches. 😂
    Gaming never changes. 🎮
    #Relatable #GamingCommunity
    ```
    or
    ```
    W update by [Studio/Game]! 👏

    Finally some good news for gamers. 🔥
    #GamingNews #𝕹𝖎𝖌𝖍𝖙
    ```
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
    🚨 Write a *fast* emotional take on a trending game update, release, bug, patch, or news.  
    Focus on a punchy reaction (positive or negative). Keep it under 270 characters.

    **Guidelines**:
    - Start with a reaction: "WHAT is this patch??", "Huge W for gamers. 👏", "Bro... what?? 😂"
    - Always pick a side (hype or hate).
    - Use 1-2 fitting hashtags like #GamingNews #TrendingGames.
    - Encourage replies if possible ("Are you trying this? 👇", "Thoughts? 🎮").

    **Example Templates**:
      ```
    🚨 [Update/Release] just dropped!

    [Quick emotional reaction / joke] 😂
    #TrendingGames #𝕹𝖎𝖌𝖍𝖙
      ```
    or
    ```
    Bro this patch note is WILD. 🤣

    [Insert most ridiculous/funny change].
    #GamingCommunity #𝕹𝖎𝖌𝖍𝖙
    ```
    """.strip(),
}

def get_prompt(content_type: ContentType) -> str:
    """Get the prompt template for a given content type"""
    return PROMPTS.get(content_type)
