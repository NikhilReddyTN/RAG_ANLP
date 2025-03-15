import json
from ics import Calendar

ics_file = "../ical_tepper.ics"  
with open(ics_file, "r",encoding="utf-8",errors="ignore") as file:
    calendar = Calendar(file.read())
events_list = []
for event in calendar.events:
    events_list.append({
        "title": event.name,
        "start": event.begin.isoformat() if event.begin else None,
        "end": event.end.isoformat() if event.end else None,
        "location": event.location,
        "description": event.description
    })
json_file = "cmu_tartan_connect.json"
with open(json_file, "w", encoding="utf-8") as file:
    json.dump(events_list, file, indent=4, ensure_ascii=False)
