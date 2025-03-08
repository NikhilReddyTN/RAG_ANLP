import requests
from bs4 import BeautifulSoup
import json

def get_team_schedule():
    # URL for the Steelers' schedule page
    url = 'https://www.steelers.com/schedule/'

    # Fetch the page content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the game elements in the page
    games = soup.find_all('div', class_='nfl-o-matchup-cards--post-game')

    # List to store game details
    game_details = []

    # Loop through each game and extract relevant info
    for game in games:
        game_info = {}

        # Extract opponent
        opponent_name = game.find('div', class_='nfl-o-matchup-cards__team-name')
        if opponent_name:
            opponent = opponent_name.find('p', class_='nfl-o-matchup-cards__team-short-name').text.strip()
            game_info['Opponent'] = opponent

        # Extract game day and week
        date_info = game.find('p', class_='nfl-o-matchup-cards__date-info')
        if date_info:
            game_day = date_info.find('span', class_='nfl-o-matchup-cards__date-info--date').text.strip()
            week_info = date_info.find('span', class_='nfl-o-matchup-cards__date-info--week').text.strip()
            game_info['Game Day'] = game_day
            game_info['Week'] = week_info

        # Extract score
        score = game.find('span', class_='nfl-o-matchup-cards__score--points')
        if score:
            game_info['Score'] = score.text.strip()

        # Check if the game was home or away
        venue = game.find('div', class_='nfl-o-matchup-cards__venue')
        if venue:
            if 'home' in venue.text.lower():
                game_info['Home/Away'] = 'Home'
            else:
                game_info['Home/Away'] = 'Away'

        # Add the game info to the list
        game_details.append(game_info)

    return game_details

def main(json_sched):
    schedule = get_team_schedule()
    with open(json_sched, "w", encoding="utf-8") as file:
        json.dump(schedule, file, ensure_ascii=False, indent=4)

    print(f"Scraping completed. Data saved to {json_sched}.")
    
if __name__ == "__main__":
    json_sched = input("Enter the output json file name for the team schedule: ")
    main(json_sched)
