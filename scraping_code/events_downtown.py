import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from tqdm import tqdm

BASE_URL = "https://downtownpittsburgh.com"

def get_description(drv, rel_url):
    url = BASE_URL + rel_url if rel_url.startswith("/") else rel_url
    drv.get(url)
    time.sleep(2)
    soup = BeautifulSoup(drv.page_source, "html.parser")
    paras = soup.find_all("p")
    desc = "\n".join(p.get_text(strip=True) for p in paras)
    return desc

def scrape_events(drv):
    soup = BeautifulSoup(drv.page_source, "html.parser")
    items = soup.find_all("div", class_="eventitem")
    evts = []
    
    for item in tqdm(items, desc="Processing events", unit="event"):
        ev_id = item.get("id", "")
        content = item.find("div", class_="copyContent")
        if not content:
            continue

        cat_div = content.find("div", class_="category")
        cats = []
        if cat_div:
            terms = cat_div.find_all("div", class_="term")
            cats = [t.get_text(strip=True).strip(",") for t in terms]

        h1 = content.find("h1")
        a = h1.find("a") if h1 else None
        title = a.get_text(strip=True) if a else ""
        d_url = a.get("href") if a else ""

        date_div = content.find("div", class_="eventdate")
        date = date_div.get_text(strip=True) if date_div else ""

        summary = content.get_text(" ", strip=True)
        for part in [", ".join(cats), title, date, "READ MORE"]:
            summary = summary.replace(part, "")
        summary = summary.strip()

        full_desc = get_description(drv, d_url) if d_url else ""

        record = {
            "id": ev_id,
            "title": title,
            "categories": cats,
            "date": date,
            "summary": summary,
            "detail_url": BASE_URL + d_url if d_url.startswith("/") else d_url,
            "full_description": full_desc
        }
        evts.append(record)
    return evts

if __name__ == "__main__":
    drv = webdriver.Chrome()
    evts = []
    for m in range(3, 13):
        url = f"{BASE_URL}/events/?n={m}&y=2025&cat=0"
        drv.get(url)
        WebDriverWait(drv, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.eventitem"))
        )
        m_evts = scrape_events(drv)
        evts.extend(m_evts)
    drv.quit()
    with open("downtown_events.json", "w", encoding="utf-8") as f:
        json.dump(evts, f, ensure_ascii=False, indent=4)
