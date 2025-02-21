import json
import logging
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

async def scraper(url):
    try:
        # Send a GET request to fetch the website content with headers - user-agent
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        response = requests.get(f"https://www.ign.com{url}", headers=headers)
        response.raise_for_status()

        # Parse the content with BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract the <title> tag
        title_tag = soup.find("title")
        title = title_tag.text if title_tag else "No title found"

        try:
            # Extract the <meta> tag with name="description"
            meta_description = soup.find("meta", attrs={"name": "description"})
            
            description = (
                meta_description["content"] if meta_description else "No description found"
            )
        except:
            pass
        
        try:
            # Extract the json data in script tag
            script_data = soup.find("script", attrs={"id": "__NEXT_DATA__"})
            if script_data:
                script_content = json.loads(script_data.text.strip())
                return script_content["props"]["pageProps"]["page"]["processedHtml"]
        except Exception as e:
            logger.error(f"Error in scraping: {e}")
            print(f"scraper - {e}")
            return
        
        return {"title": title, "description": description}

    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}