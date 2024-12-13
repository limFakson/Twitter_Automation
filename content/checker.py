import tweepy
from bs4 import BeautifulSoup
import requests
import json
from config.environment import load_environment
import logging

logger = logging.getLogger(__name__)

def configure_logging():
    logging.basicConfig(level=logging.INFO)
    logger.info("Logger configured")

def setup_twitter_api(config):
    """Setup Twitter API with provided config"""
    auth = tweepy.OAuthHandler(config["TWITTER_API_KEY"], config["TWITTER_API_SECRET"])
    auth.set_access_token(config["TWITTER_ACCESS_TOKEN"], config["TWITTER_ACCESS_SECRET"])
    return tweepy.API(auth, wait_on_rate_limit=True)

class DMListener(tweepy.StreamListener):
    def __init__(self, api, config):
        self.api = api
        self.config = config
        super().__init__(api)

    def on_direct_message(self, status):
        # Process the direct message
        if status.message_create['message_data']['text'].startswith('@Tweetauthenticitybot search:'):
            query = status.message_create['message_data']['text'].replace('@Tweetauthenticitybot search:', '').strip()
            # Simulate credibility check (Now calls the actual logic)
            credibility_info = self.check_credibility(query)
            # Respond with the credibility info
            self.api.send_direct_message(recipient_id=status.message_create['sender_id'],
                                         message=credibility_info)

    def check_credibility(self, query, original_source_url=None):
        # **Note:** original_source_url is not used in this demo but can be passed if available
        credibility_report = {
            'query': query,
            'fact_check_results': self.fact_check_query(query),
            'ource_credibility': "Not Applicable in this Demo" 
            # To assess source credibility, integrate a service API as previously discussed
        }
        return json.dumps(credibility_report, indent=4)

    def fact_check_query(self, query):
        # Google Fact Check Tools API
        api_key = self.config["CHECKER_BOT_TOKEN"]  # **Assumption:** This token is for the fact-check API
        url = f"https://factchecktools.googleapis.com/v1alpha1/claims:search?key={api_key}&query={query}&languageCode=en"
        
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'claims' in data:
                return data['claims']
            else:
                return ["No fact-check results found."]
        else:
            return [f"Failed to retrieve fact-check results. Status Code: {response.status_code}"]

def main():
    configure_logging()
    config = load_environment()
    
    # Setup Twitter API
    twitter_api = setup_twitter_api(config)
    
    # Setup Stream Listener
    listener = DMListener(twitter_api, config)
    stream = tweepy.Stream(auth=twitter_api.auth, listener=listener)
    
    # Filter for Direct Messages (Note: This might require additional permissions and setup on the Twitter Developer Dashboard)
    # As of my last update, direct message filtering isn't directly supported through the standard streaming API without specific approvals.
    # For development and testing, consider triggering the `on_direct_message` logic through other means (e.g., manually for demo purposes).
    # stream.filter(track=["@Tweetauthenticitybot"])  # **Demo Purposes Only**; Adjust based on actual Twitter API capabilities and your app's permissions.
    
    # **For Demo:** Manually trigger the credibility check to test the logic without setting up a full streaming listener.
    query = "Example Query for Credibility Check"
    credibility_info = listener.check_credibility(query)
    logger.info(f"Credibility Info for '{query}': {credibility_info}")

if __name__ == "__main__":
    main()