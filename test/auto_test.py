# import cloudscraper as CloudScraper
import requests
import json


# def test_scraper():
#     scraper = CloudScraper.CloudScraper()
#     response = scraper.get("https://www.ign.com/?filter=games")
#     assert response.status_code == 200
#     with open("test/ign.html", "w") as f:
#         f.write(response.text)


def get_data_from_api(url):
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

    responce = requests.post(url, json=params, headers=headers)
    with open("test/ign.json", "w") as f:
        f.write(str(responce.json()))
    ign_news = responce.json()
    content_feeds = ign_news["data"]["homepage"]["contentFeed"]["feedItems"]
    return content_feeds


print(get_data_from_api("https://mollusk.apis.ign.com/graphql"))

# from openai import OpenAI

# client = OpenAI(
#     api_key="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"
# )

# completion = client.chat.completions.create(
#     model="gpt-3.5-turbo",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "Write a haiku about recursion in programming."},
#     ],
# )

# print(completion.choices[0].message)

from enum import Enum
import random


# class ContentType(Enum):
#     UNITY_TIPS = "unity_tips"
#     GAME_DEV_THREAD = "game_dev_thread"
#     GAME_NEWS = "game_news"
#     GAME_DEV_POLL = "game_dev_poll"
#     GAME_DEV_MEME = "game_dev_meme"
#     GAME_DEV_JOBS = "game_dev_jobs"
#     UNITY_TUTORIAL = "unity_tutorial"
#     GAME_DESIGN = "game_design"
#     INDIE_DEV = "indie_dev"
#     GAME_MARKETING = "game_marketing"
#     GAME_NEWS_SOURCE = "game_news_source"


# content_type = random.choice(list(ContentType))
# print(content_type)
