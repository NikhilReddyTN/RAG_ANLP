import csv
import json

def get_team_schedule():
    # Initialize a list to store the results
    games = []

    # Open the CSV file and read it
    with open('schedule_NHL_2024.csv', mode='r') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            # Check if "Pittsburgh Penguins" is in either 'TEAM HOME' or 'TEAM AWAY'
            if "Pittsburgh Penguins" in row['TEAM HOME'] or "Pittsburgh Penguins" in row['TEAM AWAY']:
                # Initialize the dictionary for the current game
                game_info = {}
                
                # Extract date information
                game_info['date'] = f"{row['YEAR']}-{row['MONTH']}-{row['DAY']}"
                
                # Check if Pittsburgh Penguins is at home or away
                if "Pittsburgh Penguins" == row['TEAM HOME']:
                    game_info['home'] = True
                    game_info['opponent'] = row['TEAM AWAY']
                else:
                    game_info['home'] = False
                    game_info['opponent'] = row['TEAM HOME']
                
                # Append the dictionary to the list
                games.append(game_info)

    return games

def main(json_sched):
    schedule = get_team_schedule()
    
    with open(json_sched, "w", encoding="utf-8") as file:
        json.dump(schedule, file, ensure_ascii=False, indent=4)

    print(f"Scraping completed. Data saved to {json_sched}.")
    
if __name__ == "__main__":
    json_sched = input("Enter the output json file name for the team schedule: ")
    main(json_sched)