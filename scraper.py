import requests
from bs4 import BeautifulSoup
import random

def scrapeWikiArticle(url):
    try:
        response = requests.get(url=url)
        response.raise_for_status()  # Raise an error for bad responses

        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.find(id="firstHeading")
        print(title.text)

        allLinks = soup.find(id="bodyContent").find_all("a")
        random.shuffle(allLinks)
        linkToScrape = None

        for link in allLinks:
            # We are only interested in other wiki articles
            if link['href'].find("/wiki/") == -1: 
                continue

            # Use this link to scrape
            linkToScrape = link
            break

        if linkToScrape:
            # Ensure the URL is correctly formed
            new_url = "https://en.wikipedia.org" + linkToScrape['href']
            scrapeWikiArticle(new_url)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# Get the initial URL from the user
user_input = input("Enter a Wikipedia article URL (e.g., https://en.wikipedia.org/wiki/Web_scraping): ")
scrapeWikiArticle(user_input)