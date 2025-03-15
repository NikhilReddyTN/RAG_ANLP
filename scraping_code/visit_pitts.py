import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import json
import re

def clean_text(soup):
    for element in soup(["nav", "footer", "script", "style"]):
        element.decompose()
    text = soup.get_text()
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"[\n\t\r]", " ", text)
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    filtered_paragraphs = [p for p in paragraphs if len(p.split()) > 10]
    return filtered_paragraphs

def should_scrape(url, base_url):
    if not url.startswith("https://www.visitpittsburgh.com"):
        return False
    return url.startswith(base_url)

def scrape_page(url, base_url, visited_urls, events):
    if url in visited_urls:
        return
    visited_urls.add(url)

    print(f"Scraping: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve {url}: {e}")
        return

    soup = BeautifulSoup(response.text, "lxml")
    cleaned_paragraphs = clean_text(soup)
    title = soup.title.string if soup.title else "No Title"
    content = "\n".join(cleaned_paragraphs)
    events.append({
        "url": url,
        "title": title,
        "content": content
    })

    for link in soup.find_all("a", href=True):
        full_url = urljoin(base_url, link["href"])
        if should_scrape(full_url, base_url):
            scrape_page(full_url, base_url, visited_urls, events)
        elif not full_url.startswith("https://www.visitpittsburgh.com"):
            if full_url not in visited_urls:
                scrape_external_page(full_url, visited_urls, events)

    time.sleep(1)

def scrape_external_page(url, visited_urls, events):
    if url in visited_urls:
        return
    visited_urls.add(url)
    print(f"Scraping external page: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve {url}: {e}")
        return

    soup = BeautifulSoup(response.text, "lxml")

    cleaned_paragraphs = clean_text(soup)

    title = soup.title.string if soup.title else "No Title"
    content = "\n".join(cleaned_paragraphs)
    events.append({
        "url": url,
        "title": title,
        "content": content
    })
    time.sleep(1)

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