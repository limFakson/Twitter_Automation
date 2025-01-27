import requests
import json
from bs4 import BeautifulSoup


def scrape_meta_and_title(url):
    try:
        # Send a GET request to fetch the website content
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        response = requests.get(f"{url}", headers=headers)
        response.raise_for_status()

        # Parse the content with BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract the <title> tag
        title_tag = soup.find("title")
        title = title_tag.text if title_tag else "No title found"

        # Extract the <meta> tag with name="description"
        meta_description = soup.find("meta", attrs={"name": "description"})
        description = (
            meta_description["content"] if meta_description else "No description found"
        )

        # Extract the json data in script tag
        script_data = soup.find("script", attrs={"id": "__NEXT_DATA__"})
        if script_data:
            script_content = json.loads(script_data.text.strip())
            return script_content["props"]["pageProps"]["page"]["processedHtml"]
        # {"title": title, "description": description}
        return

    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}


# Example usage
url = "https://www.ign.com/articles/doom-the-dark-ages-has-a-release-date-and-an-explanation-for-why-its-single-player-campaign-only"  # Replace with the URL of the site you want to scrape
result = scrape_meta_and_title(url)
print(result)
