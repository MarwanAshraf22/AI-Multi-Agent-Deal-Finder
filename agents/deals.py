from pydantic import BaseModel
from typing import List, Dict
from bs4 import BeautifulSoup
import re
import feedparser
from tqdm import tqdm
import requests
import time

feeds = [
    "https://www.dealnews.com/c142/Electronics/?rss=1",
        "https://www.dealnews.com/c39/Computers/?rss=1",
        "https://www.dealnews.com/c238/Automotive/?rss=1",
        "https://www.dealnews.com/f1912/Smart-Home/?rss=1",
        "https://www.dealnews.com/c196/Home-Garden/?rss=1",
       ]

def extract(html_snippet: str) -> str:  # Function to clean HTML and extract text
    """
    Use Beautiful Soup to clean up this HTML snippet and extract useful text
    """
    soup = BeautifulSoup(html_snippet, 'html.parser')  # Parse HTML content using BeautifulSoup
    snippet_div = soup.find('div', class_='snippet summary')  # Find div with class 'snippet summary'
    
    if snippet_div:  # Check if the snippet div was found
        description = snippet_div.get_text(strip=True)  # Extract text content and strip whitespace
        description = BeautifulSoup(description, 'html.parser').get_text()  # Parse again to remove any remaining HTML
        description = re.sub('<[^<]+?>', '', description)  # Remove any remaining HTML tags using regex
        result = description.strip()  # Strip leading/trailing whitespace
    else:  # If snippet div not found
        result = html_snippet  # Use original HTML snippet as fallback
    return result.replace('\n', ' ')  # Replace newlines with spaces and return

class ScrapedDeal:  # Define class to represent a deal scraped from RSS feeds
    """
    A class to represent a Deal retrieved from an RSS feed
    """
    category: str  # Product category attribute
    title: str  # Deal title attribute
    summary: str  # Deal summary attribute
    url: str  # Deal URL attribute
    details: str  # Detailed product information attribute
    features: str  # Product features attribute

    def __init__(self, entry: Dict[str, str]):  # Constructor method
        """
        Populate this instance based on the provided dict
        """
        self.title = entry['title']  # Extract title from RSS entry
        self.summary = extract(entry['summary'])  # Clean and extract summary using extract function
        self.url = entry['links'][0]['href']  # Get URL from first link in entry
        stuff = requests.get(self.url).content  # Fetch full deal page content via HTTP request
        soup = BeautifulSoup(stuff, 'html.parser')  # Parse the fetched HTML content
        content = soup.find('div', class_='content-section').get_text()  # Find content section and extract text
        content = content.replace('\nmore', '').replace('\n', ' ')  # Clean up content by removing 'more' and newlines
        if "Features" in content:  # Check if content contains a Features section
            self.details, self.features = content.split("Features")  # Split content at Features section
        else:  # If no Features section found
            self.details = content  # Use all content as details
            self.features = ""  # Set features to empty string

    def __repr__(self):  # String representation method for debugging
        """
        Return a string to describe this deal
        """
        return f"<{self.title}>"  # Return deal title in angle brackets

    def describe(self):  # Method to create formatted description for AI models
        """
        Return a longer string to describe this deal for use in calling a model
        """
        return f"Title: {self.title}\nDetails: {self.details.strip()}\nFeatures: {self.features.strip()}\nURL: {self.url}"  # Return formatted multi-line description

    @classmethod  # Class method decorator
    def fetch(cls, show_progress : bool = False) -> List["ScrapedDeal"]:  # Class method to fetch deals from RSS feeds
        """
        Retrieve all deals from the selected RSS feeds
        """
        deals = []  # Initialize empty list to store deals
        feed_iter = tqdm(feeds) if show_progress else feeds  # Use progress bar if requested, otherwise use feeds directly
        for feed_url in feed_iter:  # Iterate through each RSS feed URL
            feed = feedparser.parse(feed_url)  # Parse the RSS feed using feedparser
            for entry in feed.entries[:10]:  # Process first 10 entries from each feed
                deals.append(cls(entry))  # Create ScrapedDeal instance and add to deals list
                time.sleep(0.5)  # Add delay to avoid overwhelming the server
        return deals  # Return list of all scraped deals

class Deal(BaseModel):  # Define Pydantic model for simplified deal representation
    """
    A class to Represent a Deal with a summary description
    """
    product_description: str  # Text description of the product
    price: float  # Deal price as floating point number
    url: str  # URL link to the deal

class DealSelection(BaseModel):  # Define Pydantic model for containing multiple deals
    """
    A class to Represent a list of Deals
    """
    deals: List[Deal]  # List of Deal objects

class Opportunity(BaseModel):  # Define Pydantic model for profitable deal opportunities
    """
    A class to represent a possible opportunity: a Deal where we estimate
    it should cost more than it's being offered
    """
    deal: Deal  # The Deal object containing product information
    estimate: float  # Estimated market value of the product
    discount: float  # Calculated discount percentage from estimated value