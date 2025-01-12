import cloudscraper as CloudScraper
import requests
import json


def test_scraper():
    scraper = CloudScraper.CloudScraper()
    response = scraper.get("https://www.ign.com/?filter=games")
    assert response.status_code == 200
    with open("test/ign.html", "w") as f:
        f.write(response.text)


test_scraper()
