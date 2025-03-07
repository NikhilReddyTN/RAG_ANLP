import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import json
import re

# Set the base URL
base_url = "# your base website here"
visited_urls = set()

# List to store scraped event data
event_data = []

def clean_text(soup):
    # Remove unwanted elements
    for element in soup(["nav", "footer", "script", "style"]):
        element.decompose()

    # Extract text
    text = soup.get_text()

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Remove special characters
    text = re.sub(r"[\n\t\r]", " ", text)

    # Split into paragraphs
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    # Filter out short sentences
    filtered_paragraphs = [p for p in paragraphs if len(p.split()) > 10]

    return filtered_paragraphs

def should_scrape(url):
    """
    Determine whether a URL should be scraped.
    - Always scrape external URLs.
    - Only scrape visitpittsburgh.com URLs that are part of the 'marathons-runs-walks' section.
    """
    if not url.startswith("# your base website here"):
        return True  # Scrape all external URLs
    # Only scrape visitpittsburgh.com URLs that are part of the 'marathons-runs-walks' section
    return url.startswith(base_url)

def scrape_page(url):
    # Skip if already visited
    if url in visited_urls:
        return
    visited_urls.add(url)

    # Fetch the page
    print(f"Scraping: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve {url}: {e}")
        return

    # Parse the page
    soup = BeautifulSoup(response.text, "lxml")

    # Clean the text
    cleaned_paragraphs = clean_text(soup)

    # Save the cleaned data to the list
    title = soup.title.string if soup.title else "No Title"
    content = "\n".join(cleaned_paragraphs)
    event_data.append({
        "url": url,
        "title": title,
        "content": content
    })

    # Extract all links on the page
    for link in soup.find_all("a", href=True):
        full_url = urljoin(base_url, link["href"])

        # Only scrape if the URL passes the filter
        if should_scrape(full_url):
            scrape_page(full_url)

    # Be polite: add a delay between requests
    time.sleep(1)

# Start scraping from the base URL
scrape_page(base_url)

# Save the scraped data to a JSON file
with open("#xxxxx.json", "w", encoding="utf-8") as file:
    json.dump(event_data, file, ensure_ascii=False, indent=4)

print("Scraping completed. Data saved to 'scraped_data.json'.")
