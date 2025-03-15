import json
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta


driver = webdriver.Chrome()  
wait = WebDriverWait(driver, 10)
base_url = "https://events.cmu.edu/"


start_date = datetime(2025, 10, 3)
end_date = datetime(2025, 10, 5)
delta = timedelta(days=1)
current_date = start_date
all_events = []

while current_date <= end_date:
    date_str = current_date.strftime("%Y%m%d")
    day_url = f"{base_url}/day/date/{date_str}"
    print(f"Processing: {day_url}")
    driver.get(day_url)
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.lw_events_title a")))
    except Exception as e:
        print(f"No events found on {date_str}: {e}")
        current_date += delta
        time.sleep(random.uniform(1, 2))
        continue
    event_links = driver.find_elements(By.CSS_SELECTOR, "div.lw_events_title a")
    event_urls = []
    for link in event_links:
        href = link.get_attribute("href")
        if not href.startswith("http"):
            href = base_url + href
        event_urls.append(href)

    for url in event_urls:
        try:
            time.sleep(random.uniform(1.5, 3.0))
            driver.execute_script("window.open(arguments[0]);", url)
            driver.switch_to.window(driver.window_handles[-1])
            
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#lw_cal_events h1")))
            
            title = driver.find_element(By.CSS_SELECTOR, "#lw_cal_events h1").text
            date_info = driver.find_element(By.CSS_SELECTOR, "#lw_cal_this_day").text
            time_location = driver.find_element(By.CSS_SELECTOR, "#lw_cal_events p").text
            description = driver.find_element(By.CSS_SELECTOR, ".lw_calendar_event_description").text
            
            event_data = {
                "title": title,
                "date": date_info,
                "time_location": time_location,
                "description": description,
                "source_url": driver.current_url
            }
            all_events.append(event_data)
            print("Scraped:", title)
        except Exception as e:
            print("Error extracting details from", url, ":", e)
        finally:
            if len(driver.window_handles) > 1:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            
            if len(all_events) % 20== 0:
                print("Pausing to avoid rate limits...")
                time.sleep(1)
    
    current_date += delta
    time.sleep(random.uniform(1, 2))

driver.quit()


with open("event_sep.json", "w", encoding="utf-8") as f:
    json.dump(all_events, f, indent=2, ensure_ascii=False)

print("Data saved to event_sep.json")
