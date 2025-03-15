import vobject
import json

# Read the ICS file
with open("/Users/heejin/Downloads/ical_tepper.ics", "r", encoding="utf-8", errors="ignore") as file:
    cal = vobject.readOne(file)

events_list = []
for event in cal.components():
    if event.name == "VEVENT":
        events_list.append({
            "title": event.summary.value if hasattr(event, "summary") else "No title",
            "start": event.dtstart.value.isoformat() if hasattr(event, "dtstart") else None,
            "end": event.dtend.value.isoformat() if hasattr(event, "dtend") else None,
            "location": event.location.value if hasattr(event, "location") else "No location",
            "description": event.description.value if hasattr(event, "description") else "No description"
        })

# Save JSON output
with open("cmu_tartan_connect.json", "w", encoding="utf-8") as file:
    json.dump(events_list, file, indent=4, ensure_ascii=False)

print("✅ ICS successfully converted to JSON!")
