import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import json
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from tqdm import tqdm
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://www.pghcitypaper.com"

def get_total_pages(driver):
    try:
        header = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "p.fdn-search-result-header"))
        )
        header_text = header.get_attribute("textContent")
        parts = header_text.split()
        total_pages = int(parts[-1])
        return total_pages
    except Exception as e:
        print("Error extracting total pages:", e)
        return 1

def scrape_events_from_page(driver):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    event_blocks = soup.find_all("div", class_="fdn-pres-content")
    events = []
    for block in tqdm(event_blocks, desc="Processing events", unit="event"):
        try:
            headline = block.find("p", class_="fdn-teaser-headline")
            if not headline:
                continue
            a_tag = headline.find("a")
            if not a_tag:
                continue
            event_title = a_tag.get_text(strip=True)
            detail_url = a_tag.get("href")
            full_detail_url = detail_url if detail_url.startswith("http") else urljoin(BASE_URL, detail_url)
            teaser = block.find("p", class_="fdn-teaser-subheadline")
            teaser_text = teaser.get_text(" ", strip=True) if teaser else ""
            location_block = block.find("div", class_="fdn-event-teaser-location-block")
            location = ""
            if location_block:
                loc_link = location_block.find("a", class_="fdn-event-teaser-location-link")
                if loc_link:
                    location = loc_link.get_text(strip=True)
            description_div = block.find("div", class_="fdn-teaser-description")
            listing_description = description_div.get_text(" ", strip=True) if description_div else ""
            event_record = {
                "title": event_title,
                "teaser": teaser_text,
                "location": location,
                "listing_description": listing_description,
                "detail_url": full_detail_url
            }
            events.append(event_record)
        except Exception as e:
            print("Error processing an event:", e)
    return events

def scrape_all_pages():
    driver = uc.Chrome()
    search_url = f"{BASE_URL}/pittsburgh/EventSearch?v=d"
    driver.get(search_url)
    total_pages = 23
    print(f"Total pages found: {total_pages}")
    all_events = []
    for page in range(1, total_pages + 1):
        print(f"\nScraping page {page} of {total_pages}")
        page_url = f"{BASE_URL}/pittsburgh/EventSearch?page={page}&v=d"
        driver.get(page_url)
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.fdn-pres-content"))
            )
        except Exception as e:
            print(f"Error waiting for events on page {page}: {e}")
            continue
        events_on_page = scrape_events_from_page(driver)
        all_events.extend(events_on_page)
        time.sleep(1)
    driver.quit()
    return all_events

def store_events_as_json(events, filename="pghcitypaper_events.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(events, f, ensure_ascii=False, indent=4)
    print(f"Stored {len(events)} events in {filename}")

if __name__ == "__main__":
    events_data = scrape_all_pages()
    store_events_as_json(events_data)
