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

def scrape_evts(drv):
    soup = BeautifulSoup(drv.page_source, "html.parser")
    blocks = soup.find_all("div", class_="fdn-pres-content")
    evts = []
    for blk in tqdm(blocks, desc="Processing events", unit="event"):
        head = blk.find("p", class_="fdn-teaser-headline")
        if not head:
            continue
        a = head.find("a")
        if not a:
            continue
        title = a.get_text(strip=True)
        d_url = a.get("href")
        full_url = d_url if d_url.startswith("http") else urljoin(BASE_URL, d_url)
        sub = blk.find("p", class_="fdn-teaser-subheadline")
        teaser = sub.get_text(" ", strip=True) if sub else ""
        loc_blk = blk.find("div", class_="fdn-event-teaser-location-block")
        loc = ""
        if loc_blk:
            link = loc_blk.find("a", class_="fdn-event-teaser-location-link")
            if link:
                loc = link.get_text(strip=True)
        desc_blk = blk.find("div", class_="fdn-teaser-description")
        desc = desc_blk.get_text(" ", strip=True) if desc_blk else ""
        rec = {
            "title": title,
            "teaser": teaser,
            "location": loc,
            "listing_description": desc,
            "detail_url": full_url
        }
        evts.append(rec)
    return evts   

if __name__ == "__main__":
    drv = uc.Chrome()
    s_url = f"{BASE_URL}/pittsburgh/EventSearch?v=d"
    drv.get(s_url)
    pages = 23
    print(f"Total pages found: {pages}")
    all_evts = []
    for p in range(1, pages + 1):
        print(f"\nScraping page {p} of {pages}")
        p_url = f"{BASE_URL}/pittsburgh/EventSearch?page={p}&v=d"
        drv.get(p_url)
        WebDriverWait(drv, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.fdn-pres-content"))
        )
        evts = scrape_evts(drv)
        all_evts.extend(evts)
        time.sleep(1)
    drv.quit()
    with open("paper_events.json", "w", encoding="utf-8") as f:
        json.dump(all_evts, f, ensure_ascii=False, indent=4)
    print(f"Stored {len(all_evts)} events in pghcitypaper_events.json")
