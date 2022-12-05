from wcdeetlist.tools import get_all_dragons_full_data
import json

dragons = get_all_dragons_full_data()

with open("dragons.json", "w+") as buffer:
    json.dump(heroic_race_data, buffer)