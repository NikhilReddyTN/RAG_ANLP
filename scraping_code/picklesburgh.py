from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

url = "https://www.picklesburgh.com"
driver.get(url)
time.sleep(3)

links = [a.get_attribute("href") for a in driver.find_elements(By.TAG_NAME, "a") if a.get_attribute("href")]

visited_links = set()
data = {}

def scrape_page(page_url):
    if page_url in visited_links:
        return
    visited_links.add(page_url)
    driver.get(page_url)
    time.sleep(3)
    
    text_content = driver.find_element(By.TAG_NAME, "body").text
    data[page_url] = text_content
    
    new_links = [a.get_attribute("href") for a in driver.find_elements(By.TAG_NAME, "a") if a.get_attribute("href")]
    
    for link in new_links:
        if link.startswith("https://www.picklesburgh.com"):
            scrape_page(link)

scrape_page(url)

driver.quit()

with open("picklesburgh_data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("Scraping completed. Data saved to picklesburgh_data.json")