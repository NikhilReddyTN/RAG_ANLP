import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from tqdm import tqdm

BASE_URL = "https://downtownpittsburgh.com"

def get_event_detail(driver, detail_relative_url):
    full_url = BASE_URL + detail_relative_url if detail_relative_url.startswith("/") else detail_relative_url
    try:
        driver.get(full_url)
        time.sleep(2)
        detail_soup = BeautifulSoup(driver.page_source, "html.parser")
        paragraphs = detail_soup.find_all("p")
        description = "\n".join(p.get_text(strip=True) for p in paragraphs)
        return description
    except Exception as e:
        print(f"Error fetching detail from {full_url}: {e}")
        return ""

def scrape_events_for_current_page(driver):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    event_items = soup.find_all("div", class_="eventitem")
    events = []
    
    for item in tqdm(event_items, desc="Processing events", unit="event"):
        try:
            event_id = item.get("id", "")
            copy_content = item.find("div", class_="copyContent")
            if not copy_content:
                continue

            category_div = copy_content.find("div", class_="category")
            categories = []
            if category_div:
                terms = category_div.find_all("div", class_="term")
                categories = [term.get_text(strip=True).strip(",") for term in terms]

            h1 = copy_content.find("h1")
            a_tag = h1.find("a") if h1 else None
            event_title = a_tag.get_text(strip=True) if a_tag else ""
            detail_url = a_tag.get("href") if a_tag else ""

            event_date_div = copy_content.find("div", class_="eventdate")
            event_date = event_date_div.get_text(strip=True) if event_date_div else ""

            summary = copy_content.get_text(" ", strip=True)
            for part in [", ".join(categories), event_title, event_date, "READ MORE"]:
                summary = summary.replace(part, "")
            summary = summary.strip()

            full_description = get_event_detail(driver, detail_url) if detail_url else ""

            event_record = {
                "id": event_id,
                "title": event_title,
                "categories": categories,
                "date": event_date,
                "summary": summary,
                "detail_url": BASE_URL + detail_url if detail_url.startswith("/") else detail_url,
                "full_description": full_description
            }
            events.append(event_record)
        except Exception as e:
            print("Error processing an event:", e)
    return events

def scrape_downtown_events():
    driver = webdriver.Chrome()
    all_events = []
    
    for month in range(3, 13):
        url = f"{BASE_URL}/events/?n={month}&y=2025&cat=0"
        print(f"\nScraping events for month {month} using URL: {url}")
        driver.get(url)
        
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.eventitem"))
            )
        except Exception as e:
            print(f"No events loaded for month {month} or error: {e}")
            continue

        month_events = scrape_events_for_current_page(driver)
        all_events.extend(month_events)
    driver.quit()
    return all_events

def store_events_as_json(events, filename="downtown_events.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(events, f, ensure_ascii=False, indent=4)
    print(f"Stored {len(events)} events in {filename}")

if __name__ == "__main__":
    events_data = scrape_downtown_events()
    store_events_as_json(events_data)
