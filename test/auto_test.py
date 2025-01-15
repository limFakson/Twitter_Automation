import cloudscraper as CloudScraper
import requests
import json


def test_scraper():
    scraper = CloudScraper.CloudScraper()
    response = scraper.get("https://www.ign.com/?filter=games")
    assert response.status_code == 200
    with open("test/ign.html", "w") as f:
        f.write(response.text)


def get_data_from_api(url):
    params = {
        "operationName": "HomepageContentFeed",
        "variables": {"filter": "Latest", "startIndex": 0, "newsOnly": False},
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
    return responce.json


print(get_data_from_api("https://mollusk.apis.ign.com/graphql"))
