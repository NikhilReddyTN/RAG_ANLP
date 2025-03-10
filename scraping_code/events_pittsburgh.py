import json
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from tqdm import tqdm  

def scrape_events():
    url = "https://pittsburgh.events/"
    drv = webdriver.Chrome()
    drv.get(url)

    wt = WebDriverWait(drv, 10)
    wt.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.dates-list")))

    while True:
        try:
            more_btn = wt.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.ldm")))
            more_btn.click()
            time.sleep(2) 
        except Exception as e:
            break

    src = drv.page_source
    drv.quit()

    soup = BeautifulSoup(src, "html.parser")
    evts = []
    rows = soup.select("ul.dates-list li.date-row")
    for li in tqdm(rows, desc="Processing events", unit="event"):
        mon = li.select_one("div.date .month").get_text(strip=True)
        day = li.select_one("div.date .day").get_text(strip=True)
        yr = li.select_one("div.date .year").get_text(strip=True)
        t_txt = li.select_one("div.time").contents[0].strip()

        evt_a = li.select_one("div.venue a")
        evt_nm = evt_a.get_text(strip=True)
        evt_url = evt_a.get("href")

        ven_a = li.select_one("div.venue .date-desc a")
        ven_nm = ven_a.get_text(strip=True) if ven_a else ""

        loc_sp = li.select_one("div.venue span.location")
        loc_txt = loc_sp.get_text(strip=True) if loc_sp else ""

        price_div = li.select_one("div.from-price")
        price = price_div.get_text(strip=True) if price_div else ""

        desc = ""
        hdrs = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
        }
        resp = requests.get(evt_url, headers=hdrs, timeout=10)
        resp.raise_for_status()  
        d_soup = BeautifulSoup(resp.content, "html.parser")
        d_div = d_soup.select_one("div.descritpion")
        if d_div:
            desc = d_div.get_text(separator=" ", strip=True)

        rec = {
            "name": evt_nm,
            "date": f"{mon} {day}, {yr} {t_txt}",
            "venue": ven_nm,
            "location": loc_txt,
            "price": price,
            "event_url": evt_url,
            "description": desc
        }
        evts.append(rec)
    return evts
    
if __name__ == "__main__":
    evts = scrape_events()
    with open("pittsburgh_events.json", "w", encoding="utf-8") as f:
        json.dump(evts, f, ensure_ascii=False, indent=4)
    print(f"Stored {len(evts)} events in pittsburgh_events.json")
