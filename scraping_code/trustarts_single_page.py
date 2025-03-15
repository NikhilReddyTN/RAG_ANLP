import json
from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_single_page():

    driver = webdriver.Chrome()
    single_page_url = "https://trustarts.org/calendar?genre=All+Genres&organization_id=4&start_date=2025%2F03%2F15&end_date=2025%2F12%2F31&filter%5Bmin%5D=2025-03-15T01%3A58%3A19-04%3A00&filter%5Bmax%5D=2026-09-15+01%3A58%3A19+-0400&filter%5Bcurrent_page%5D=production"
    driver.get(single_page_url)
    wait = WebDriverWait(driver, 10)
    

    try:
        cookie_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button#accept-cookies"))
        )
        cookie_button.click()
    except Exception:
        pass  
    
    try:
        event_cards = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article.event"))
        )
    except Exception as e:
        print("Could not find event cards on this page:", e)
        driver.quit()
        return
    
    print(f"Found {len(event_cards)} event cards on this page.")
    
    events_data = []
    

    for card in event_cards:
        try:
            link_element = card.find_element(By.CSS_SELECTOR, "a")
            relative_url = link_element.get_attribute("href")
            event_url = urljoin("https://trustarts.org", relative_url)
        except Exception as e:
            print("Error extracting event URL:", e)
            event_url = None
        
        try:
            title = card.find_element(By.CSS_SELECTOR, ".title").text.strip()
        except Exception:
            title = None
        
        try:
            time_element = event.find_element(By.CSS_SELECTOR, ".time-wrapper time")
            event_date = time_element.get_attribute("datetime")
        except Exception:
            event_date = None

        try:
            venue_element = card.find_element(By.CSS_SELECTOR, ".venue")
            venue = venue_element.text.strip()
        except Exception:
            venue = None
        
        event_record = {
            "event_url": event_url,
            "title": title,
            "date": event_date,
            "venue": venue
        }
        events_data.append(event_record)

    driver.quit()
    with open("trustarts_opera.json", "w", encoding="utf-8") as f:
        json.dump(events_data, f, indent=2, ensure_ascii=False)
    
    print("Scraping complete. Data saved to single_page_events.json.")

if __name__ == "__main__":
    scrape_single_page()
