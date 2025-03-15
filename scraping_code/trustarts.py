import json
import time
from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_events():
    driver = webdriver.Chrome()
    base_url = "https://trustarts.org/calendar?genre=All+Genres&organization_id=5&start_date=2025%2F03%2F15&end_date=2025%2F12%2F31&filter%5Bmin%5D=2025-03-15T01%3A54%3A44-04%3A00&filter%5Bmax%5D=2026-09-15+01%3A54%3A44+-0400&filter%5Bcurrent_page%5D=production"
    events_data = []
    
    wait = WebDriverWait(driver, 15)
    

    for page in range(1, 3):
        if page == 1:
            url = base_url + "/calendar"
        else:
            url = base_url + f"/calendar?page={page}"
        print(f"Scraping page {page}: {url}")
        driver.get(url)
        

        try:
            cookie_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button#accept-cookies"))
            )
            cookie_button.click()
        except Exception:
            pass
        
        # Wait for the event articles to load
        try:
            event_elements = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article.event"))
            )
        except Exception as e:
            print(f"Could not find events on page {page}: {e}")
            continue

        print(f"Found {len(event_elements)} events on page {page}.")
        
        # Loop through each event on the current page
        for event in event_elements:
            try:
                link_element = event.find_element(By.CSS_SELECTOR, "a.lead-image-link")
                relative_url = link_element.get_attribute("href")
                event_url = urljoin(base_url, relative_url)
            except Exception as e:
                print("Error extracting event URL:", e)
                event_url = None
            
            try:
                title = event.find_element(By.CSS_SELECTOR, "h3.title a").text.strip()
            except Exception:
                title = None
            try:
                time_element = event.find_element(By.CSS_SELECTOR, ".time-wrapper time")
                event_date = time_element.get_attribute("datetime")
            except Exception:
                event_date = None
            try:
                venue = event.find_element(By.CSS_SELECTOR, "div.venue").text.strip()
            except Exception:
                venue = None
            try:
                organization = event.find_element(By.CSS_SELECTOR, "div.organization").text.strip()
            except Exception:
                organization = None
            try:
                category_elements = event.find_elements(By.CSS_SELECTOR, "ul.category-group li.category a")
                categories = [cat.text.strip() for cat in category_elements]
            except Exception:
                categories = []
        
            
            event_record = {
                "event_url": event_url,
                "title": title,
                "date": event_date,
                "venue": venue,
                "organization": organization,
                "categories": categories,
               
            }
            events_data.append(event_record)
    
    driver.quit()
    

    with open("trustarts_pittsburgh_public_theatre.json", "w", encoding="utf-8") as f:
        json.dump(events_data, f, indent=2, ensure_ascii=False)
    print("Scraping complete. Events saved to events.json.")

if __name__ == "__main__":
    scrape_events()
