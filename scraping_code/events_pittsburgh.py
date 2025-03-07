import json
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from tqdm import tqdm  

def scrape_pittsburgh_events():
    url = "https://pittsburgh.events/"
    driver = webdriver.Chrome()
    driver.get(url)

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.dates-list")))

    while True:
        try:
            show_more = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.ldm")))
            show_more.click()
            time.sleep(2) 
        except Exception as e:
            print("No more 'Show More' button found or error encountered:", e)
            break

    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, "html.parser")
    events = []
    event_rows = soup.select("ul.dates-list li.date-row")
    for li in tqdm(event_rows, desc="Processing events", unit="event"):
        try:
            month = li.select_one("div.date .month").get_text(strip=True)
            day = li.select_one("div.date .day").get_text(strip=True)
            year = li.select_one("div.date .year").get_text(strip=True)
            time_text = li.select_one("div.time").contents[0].strip()

            event_anchor = li.select_one("div.venue a")
            event_name = event_anchor.get_text(strip=True)
            event_url = event_anchor.get("href")

            venue_anchor = li.select_one("div.venue .date-desc a")
            venue_name = venue_anchor.get_text(strip=True) if venue_anchor else ""

            location_span = li.select_one("div.venue span.location")
            location_text = location_span.get_text(strip=True) if location_span else ""

            price_div = li.select_one("div.from-price")
            price_text = price_div.get_text(strip=True) if price_div else ""

            event_description = ""
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
                }
                response = requests.get(event_url, headers=headers, timeout=10)
                response.raise_for_status()  
                detail_soup = BeautifulSoup(response.content, "html.parser")
                desc_div = detail_soup.select_one("div.descritpion")
                if desc_div:
                    event_description = desc_div.get_text(separator=" ", strip=True)
            except Exception as ex:
                print(f"Error fetching description for {event_url}: {ex}")

            event_record = {
                "name": event_name,
                "date": f"{month} {day}, {year} {time_text}",
                "venue": venue_name,
                "location": location_text,
                "price": price_text,
                "event_url": event_url,
                "description": event_description
            }
            events.append(event_record)
        except Exception as e:
            print("Error processing an event:", e)

    return events

def store_events_as_json(events, filename="pittsburgh_events.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(events, f, ensure_ascii=False, indent=4)
    print(f"Stored {len(events)} events in {filename}")

if __name__ == "__main__":
    events_data = scrape_pittsburgh_events()
    store_events_as_json(events_data)
