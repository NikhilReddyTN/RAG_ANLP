## Data annotation contributions from each team member

Annabelle: generated 400 question and answers set from 20MB data scraped, including visit pittsburgh, city paper journal, cmu in person events, all pittsburgh government file (tax and operating cost), all pittsburgh museums, pittsburgh symphonmy, pittsburgh orchestra, trustarts.org, warhol, tacofest, cmu scs events, cmu admission events.

Avi: generated 100 questions from the sports dataset including penguins and steelers.

## Data collection from each team member
Annabelle scraped:  banana.json carnegie_arts_museum.json carnegie_natural_history_museum.json carnegie_science_center.json city_paper_arts_entertainment.json city_paper_bestof.json city_paper_brook_drinks.json city_paper_columns.json cmu_family_weekend.json cmu_in_person_events.json cmu_scs_careerfair.json cmu_spring_carnival.json cmu_commencement.json events_arts.json events_education.json events_family.json events_food.json events_fun.json events_in_person.json events_online.json events_outdoors.json events_sports.json events_tech.json operating_budget.json pitt_cs.json pitts_museum.json pitts_park.json pitts_march_week.json taeon.json trustarts_aug_show.json trustarts_july.json trustarts_opera.json trustarts_omh.json trustarts_public_theatre.json visit_pitts_animals_events.json visit_pitts_cannabis.json visit_pitts_family_fun.json visit_pitts_fine_festivals.json visit_pitts_free_things_to_do.json visit_pitts_fall_halloween.json visit_pitts_halloween_events.json visit_pitts_holiday_wellness.json visit_pitts_hotels_resorts.json visit_pitts_marathons.json visit_pitts_meetings_events.json visit_pitts_neighborhod.json visit_pitts_outdoor_adventure.json visit_pitts_plan_your_trip.json visit_pitts_restaurants_culinary.json visit_pitts_shops.json visit_pitts_sports_to_arts.json visit_pitts_things_to_do_arts_culture.json visit_pitts_things_to_do_daycation.json visit_pitts_things_to_do_shopping.json visit_pitts_this_week_in_pittsburgh.json warhol.json

Nikhil: paper_events.json pittsburgh_britannica.json pittsburgh_events.json pittsburgh_history.json pittsburgh_wikipedia.json

Avi: sports.json steelers_roster.json steelers_schedule.json pnc_park_info.json pirates_schedule.json pirates_other.json penguins_schedule.json


## Modeling contributions from each team member
Nikhil: wrote rag.py to call the model from the Hugging Face. Setup the prompt required to generate the answers to the questions in hand. 

Avi: wrote evaluation_metrics.py for the various evaluation metrics, including average recall, average F1 score and average sentence similarity. 

Annabelle: experimented with different models of various sizes to see how they fare against our chosen model.