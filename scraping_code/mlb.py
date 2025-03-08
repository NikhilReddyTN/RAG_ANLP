import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import re
from urllib.parse import urljoin
import json
import pandas as pd

def get_soup(url):
    """Fetch page content and return BeautifulSoup object."""
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    return None

def get_selenium_soup(url):
    """Use Selenium to render JavaScript-heavy pages and return BeautifulSoup object."""
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(3)
    page_source = driver.page_source
    driver.quit()
    return BeautifulSoup(page_source, 'html.parser')

def get_team_schedule():
    df = pd.read_csv('../input/pirates_games.csv')

    # Extract date, time, opponent, and home/away status
    game_info = []

    for _, row in df.iterrows():
        # Split the opponent and home/away information from the subject
        subject = row['SUBJECT']
        date = row['START DATE']
        time = row['START TIME']
        if "at" in subject:
            opponent, location = subject.split(" at ")
            home_away = "Home" if "Pirates" in location else "Away"
        else:
            opponent = subject
            location = row['LOCATION']
            home_away = "Home" if "Pirates" in location else "Away"
        
        game_info.append({
            "Date": date,
            "Time": time,
            "Opponent": opponent,
            "Home/Away": home_away
        })
    return game_info

def get_other_static_info():
    """Scrape other relevant static information."""
    base_url = "https://www.mlb.com/pirates"
    soup = get_soup(base_url)
    static_info = []
    
    # Identify subpages
    links = set()
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith('/') and not re.search(r'(news|stats|scores)', href):
            full_url = urljoin(base_url, href)
            links.add(full_url)
    
    # Scrape each subpage once
    for link in links:
        sub_soup = get_soup(link)
        if sub_soup:
            # Organize the static information in a more meaningful structure
            page_title = sub_soup.title.text.strip() if sub_soup.title else "No Title"
            page_content = sub_soup.get_text(separator=' ', strip=True)
            
            static_info.append({
                "page_url": link,
                "page_title": page_title,
                "content": page_content
            })
    
    return static_info

def main(json_sched, json_other):
    schedule = get_team_schedule()
    other_info = get_other_static_info()
    
    with open(json_sched, "w", encoding="utf-8") as file:
        json.dump(schedule, file, ensure_ascii=False, indent=4)
    with open(json_other, "w", encoding="utf-8") as file:
        json.dump(other_info, file, ensure_ascii=False, indent=4)

    print(f"Scraping completed. Data saved to {json_sched, json_other}.")
    
if __name__ == "__main__":
    json_sched = input("Enter the output json file name for the team schedule: ")
    json_other = input("Enter the output json file name for all other info: ")
    main(json_sched, json_other)