from wcdeetlist.tools import get_dragon_full_data
import json

data = get_dragon_full_data("https://deetlist.com/dragoncity/dragon/highcolony")

print(json.dumps(data, indent=4))