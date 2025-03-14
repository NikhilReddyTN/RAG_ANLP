import csv
import json

def get_team_schedule():
    games = []

    with open('schedule_NHL_2024.csv', mode='r') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            if "Pittsburgh Penguins" in row['TEAM HOME'] or "Pittsburgh Penguins" in row['TEAM AWAY']:
                game_info = {}
                
                game_info['date'] = f"{row['YEAR']}-{row['MONTH']}-{row['DAY']}"
                
                if "Pittsburgh Penguins" == row['TEAM HOME']:
                    game_info['home'] = True
                    game_info['opponent'] = row['TEAM AWAY']
                else:
                    game_info['home'] = False
                    game_info['opponent'] = row['TEAM HOME']
                
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