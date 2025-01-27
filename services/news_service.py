import requests
import json
import os
import logging
from datetime import datetime
from utils.scraper import scraper
from asgiref.sync import async_to_sync

logger = logging.getLogger(__name__)

class NewsService:
    def __init__(self):
        self.url = "https://mollusk.apis.ign.com/graphql"
        self.content_dir = "logs/news_id"
        self.file_path = os.path.join(self.content_dir, "uploaded.txt")

    def games_news(self) -> dict:
        params = {
            "operationName": "HomepageContentFeed",
            "variables": {"filter": "Games", "startIndex": 0, "newsOnly": False},
            "extensions": {
                "persistedQuery": {
                    "version": 1,
                    "sha256Hash": "6b442d2f8fc537c15b1fb67a2221ed3eca4e06c4b85e7818a220968cd917f0ae",
                }
            },
        }
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Python-Requests",
        }

        responce = requests.post(self.url, json=params, headers=headers)
        ign_news = responce.json()
        content_feeds = ign_news["data"]["homepage"]["contentFeed"]["feedItems"]
        news_params = None
        for feeds in content_feeds:
            news_feed = feeds["content"]
            if not self.id_exists(news_feed["id"]):
                news_description = async_to_sync(scraper)(news_feed["url"])
                news_image = (
                    news_feed["feedImage"]["url"]
                    if news_feed["feedImage"]["url"] is not None
                    else None
                )
                async_to_sync(self.write_post_log)(news_feed["id"])
                news_params = {
                    "title": news_feed["title"],
                    "image": news_image,
                    "description": news_description,
                }
            else:
                logger.error(f"No recent news for now")
                return 
            break  # Get news info only once
        return news_params

    async def write_post_log(self, id) -> bool:
        # Checks if dir exists to create one
        if not os.path.exists(self.content_dir):
            os.makedirs(self.content_dir, exist_ok=True)

        # Checks if filepath exists to create one
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                f.write(
                    f"Starting post tracks for IGN - {datetime.now().isoformat()} \n"
                )

        # Write new uploaded id into txt to keep track
        with open(self.file_path, "a") as f:
            f.write(f"{datetime.now().isoformat()} - {id} \n")

        return True

    def id_exists(self, id_to_check) -> bool:
        """Checks if id already used before to generate post"""
        try:
            with open(self.file_path, "r") as f:
                for line in f:
                    if id_to_check in line:
                        return True
        except FileNotFoundError:
            return False
        return False
