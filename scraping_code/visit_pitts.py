import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import json
import re

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

def should_scrape(url, base_url):
    """
    Determine whether a URL should be scraped.
    - Only scrape visitpittsburgh.com URLs that are part of the 'marathons-runs-walks' section.
    - External URLs are scraped but not followed.
    """
    # Only scrape visitpittsburgh.com URLs that are part of the 'marathons-runs-walks' section
    return url.startswith(base_url)

def scrape_page(url, base_url, visited_urls, events):
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
    events.append({
        "url": url,
        "title": title,
        "content": content
    })

    # Extract all links on the page
    for link in soup.find_all("a", href=True):
        full_url = urljoin(base_url, link["href"])

        # Only scrape if the URL passes the filter
        if should_scrape(full_url, base_url):
            scrape_page(full_url, base_url, visited_urls, events)
        elif not full_url.startswith(base_url):
            # Scrape external URLs but do not follow them
            if full_url not in visited_urls:
                scrape_external_page(full_url, visited_urls, events)

    # Be polite: add a delay between requests
    time.sleep(1)

def scrape_external_page(url, visited_urls, events):
    # Skip if already visited
    if url in visited_urls:
        return
    visited_urls.add(url)

    # Fetch the external page
    print(f"Scraping external page: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve {url}: {e}")
        return

    # Parse the external page
    soup = BeautifulSoup(response.text, "lxml")

    # Clean the text
    cleaned_paragraphs = clean_text(soup)

    # Save the cleaned data to the list
    title = soup.title.string if soup.title else "No Title"
    content = "\n".join(cleaned_paragraphs)
    events.append({
        "url": url,
        "title": title,
        "content": content
    })

    # Be polite: add a delay between requests
    time.sleep(1)

# Start scraping from the base URL
def main(base_url, json_name):
    visited_urls = set()
    events = []

    scrape_page(base_url, base_url, visited_urls, events)
    with open(json_name, "w", encoding="utf-8") as file:
        json.dump(events, file, ensure_ascii=False, indent=4)

    print(f"Scraping completed. Data saved to {json_name}.")

if __name__ == "__main__":
    base_url = input("Enter the base url: ")
    json_name = input("Enter the output json file name: ")
    main(base_url, json_name)