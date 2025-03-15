import json
import time
import requests
import pdfplumber
from urllib.parse import urlparse, urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os

opts = Options()
opts.add_argument("--headless")
drv = webdriver.Chrome(options=opts)

def scrape(url):
    def is_pdf(u):
        return u.lower().endswith(".pdf")
    if is_pdf(url):
        print(f"Scraping PDF: {url}")
        tmp_pdf = "tmp.pdf"
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            with open(tmp_pdf, "wb") as f:
                f.write(r.content)
            txt = ""
            with pdfplumber.open(tmp_pdf) as p:
                for pg in p.pages:
                    pg_txt = pg.extract_text()
                    if pg_txt:
                        txt += pg_txt + "\n"
            os.remove(tmp_pdf)
            return {"url": url, "content": txt, "type": "pdf"}
        except Exception as e:
            print(f"Error scraping PDF {url}: {e}")
            if os.path.exists(tmp_pdf):
                os.remove(tmp_pdf)
            return None
    else:
        print(f"Scraping HTML: {url}")
        try:
            drv.get(url)
            time.sleep(2)
            pars = drv.find_elements(By.XPATH, "//p")
            txt = "\n".join([p.text for p in pars if p.text.strip()])
            return {"url": url, "content": txt, "type": "html"}
        except Exception as e:
            print(f"Error scraping HTML {url}: {e}")
            return None

def crawl(start_url, depth=1):
    visited = set()
    data = []
    def same_domain(base, link):
        return urlparse(base).netloc == urlparse(link).netloc or not urlparse(link).netloc
    def dfs(u, lvl):
        if u in visited or lvl < 0:
            return
        visited.add(u)
        item = scrape(u)
        if item:
            data.append(item)
        if item and item.get("type") == "html" and lvl > 0:
            anchors = drv.find_elements(By.TAG_NAME, "a")
            for a in anchors:
                href = a.get_attribute("href")
                if href:
                    link = urljoin(u, href)
                    if same_domain(u, link):
                        dfs(link, lvl - 1)
    dfs(start_url, depth)
    return data

if __name__ == "__main__":
    urls = ["https://www.britannica.com/place/Pittsburgh"]
    lvl = 0
    all_data = []
    for link in urls:
        all_data.extend(crawl(link, lvl))
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)
    print(f"Scraped {len(all_data)} total pages.")
    drv.quit()
