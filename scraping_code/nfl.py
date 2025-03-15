import requests
from bs4 import BeautifulSoup
import json, csv

def get_team_schedule():
    url = 'https://www.steelers.com/schedule/'

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    games = soup.find_all('div', class_='nfl-o-matchup-cards--post-game')

    game_details = []

    for game in games:
        game_info = {}

        opponent_name = game.find('div', class_='nfl-o-matchup-cards__team-name')
        if opponent_name:
            opponent = opponent_name.find('p', class_='nfl-o-matchup-cards__team-short-name').text.strip()
            game_info['Opponent'] = opponent

        date_info = game.find('p', class_='nfl-o-matchup-cards__date-info')
        if date_info:
            game_day = date_info.find('span', class_='nfl-o-matchup-cards__date-info--date').text.strip()
            week_info = date_info.find('span', class_='nfl-o-matchup-cards__date-info--week').text.strip()
            game_info['Game Day'] = game_day
            game_info['Week'] = week_info

        score = game.find('span', class_='nfl-o-matchup-cards__score--points')
        if score:
            game_info['Score'] = score.text.strip()

        venue = game.find('div', class_='nfl-o-matchup-cards__venue')
        if venue:
            if 'home' in venue.text.lower():
                game_info['Home/Away'] = 'Home'
            else:
                game_info['Home/Away'] = 'Away'

        game_details.append(game_info)

    return game_details

def get_team_roster():
    input_csv = "steelers_players.csv"
    output_json = "steelers_roster.json"

    players = []
    with open(input_csv, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["Player"] and row["Pos"]:
                player = {
                    "Name": row["Player"].strip(),
                    "Number": int(row["No."].strip()) if row["No."].strip().isdigit() else None,
                    "Pos": row["Pos"].strip(),
                    "College": row["College/Univ"].strip()
                }
                players.append(player)

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(players, f, indent=4)

    print(f"Processed {len(players)} players and saved to {output_json}")

def main(json_sched):
    schedule = get_team_schedule()
    with open(json_sched, "w", encoding="utf-8") as file:
        json.dump(schedule, file, ensure_ascii=False, indent=4)

    get_team_roster()

    print(f"Scraping completed. Data saved to {json_sched}.")
    
if __name__ == "__main__":
    json_sched = input("Enter the output json file name for the team schedule: ")
    main("")
