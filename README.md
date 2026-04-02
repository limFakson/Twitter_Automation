# Twitter Automation Platform

A Python-based SaaS platform for automating news and content sharing on Twitter (X) and Telegram.

## Architecture Overview
- **Backend**: Python with FastAPI/Flask (server.py exists).
- **Automation**: APScheduler for scheduled jobs.
- **Services**:
    - `TwitterService`: Handles Twitter API v2 interactions and media uploads.
    - `NewsService`: Scrapes and fetches latest gaming news from IGN.
    - `TelegramService`: Manages Telegram bot interactions.
    - `GeminiService`: Content generation using Google's Gemini AI.
- **Data Flow**: Fetches news -> Generates content/images -> Posts to Twitter/Telegram.

## Installation Instructions
1. Clone the repository.
2. Create a virtual environment: `python -m venv venv`
3. Activate venv: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Configure `.env` file with API keys.
6. Run the application: `python main.py`

## Commands Used During Development
- `pip install -r requirements.txt`: Install project dependencies.
- `python main.py`: Start the main automation service and scheduler.

## Feature Explanations
- **Automated News Posting**: Periodically fetches gaming news and posts them as tweets and Telegram messages.
- **Chunked Media Upload**: Custom implementation for uploading media to Twitter API v1.1 for use with v2 tweets.
- **AI Content Generation**: Uses Gemini to generate engaging tweets from news descriptions.
- **Resilient Posting**: Includes retry logic (exponential backoff) and media processing delays to handle Twitter API `503 Service Unavailable` errors.

## API Overview
- Main interaction with Twitter is via Tweepy (v2) and manual OAuth1 for media.
- IGN GraphQL API for news fetching.

## Theme System
*(To be implemented/detailed if applicable)*
