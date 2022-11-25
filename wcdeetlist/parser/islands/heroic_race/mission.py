from bs4 import BeautifulSoup
from typing import Union, List
from datetime import datetime

from ....config import (
    MINUTES_PER_HOUR,
    SECONDS_PER_DAY,
    SECONDS_PER_HOUR,
    SECONDS_PER_MINUTE
)

MISSON_TYPES = {
    "Collect Food": "food",
    "Battle Dragons": "battle",
    "Hatch Eggs": "hatch",
    "Breed Dragons": "breed",
    "Feed Dragons": "feed",
    "League Battles": "pvp",
    "Collect Gold": "gold",
}

def pool_time_to_seconds(pool_time: str) -> int:
        pool_time = pool_time.lower()

        if pool_time == "instant" or pool_time == "no minimum":
            return 0
        
        if "minutes" in pool_time:
            if "60" in pool_time:
                return 60 * SECONDS_PER_MINUTE
                
            minutes = datetime.strptime(pool_time, "%M minutes").minute
            return minutes * SECONDS_PER_MINUTE

        elif "hours" in pool_time:
            hours = datetime.strptime(pool_time, "%H hours").hour
            return hours * SECONDS_PER_HOUR

        elif "hr" in pool_time and "min" in pool_time:
            hours_and_minutes = datetime.strptime(pool_time, "%Hhr %Mmin")
            hours = hours_and_minutes.hour
            minutes = hours_and_minutes.minute

            return (hours * SECONDS_PER_HOUR) + (minutes * SECONDS_PER_MINUTE)

        elif "day" in pool_time:
            days_and_hours = datetime.strptime(pool_time, "%d day %H hrs")
            days = days_and_hours.day
            hours = days_and_hours.hour
            return (days * SECONDS_PER_DAY) + (hours * MINUTES_PER_HOUR)

class MissionParser:
    def __init__(
        self,
        mission_soup: BeautifulSoup
    ) -> None:
        self.mission_soup = mission_soup

        self.info_divs = mission_soup.select("div.m2")

    def get_type(self) -> str:
        name = self.get_name()

        return MISSON_TYPES[name]

    def get_name(self) -> str:
        name = self.mission_soup.select_one("div.mh").text
        return name

    def get_goal_items(self) -> int:
        goal_items = self.info_divs[0].text
        return int(goal_items)

    def get_pool_size(self) -> int:
        pool = self.info_divs[1].text
        return int(pool)
  
    def get_pool_time(self) -> int:
        pool_time = self.info_divs[2].text
        pool_time_seconds = pool_time_to_seconds(pool_time)
        return pool_time_seconds

    def get_item_drop_chance(self) -> str:
        drop_chance = self.info_divs[3].text
        return drop_chance

    def get_total_pool_time(self) -> int:
        total_pool_time = self.info_divs[4].text
        total_pool_time_seconds = pool_time_to_seconds(total_pool_time)
        return total_pool_time_seconds

    def get_all(self) -> dict:
        mission_type = self.get_type()
        mission_name = self.get_name()
        goal_items = self.get_goal_items()
        pool_size = self.get_pool_size()
        pool_time = self.get_pool_time()
        total_pool_time = self.get_total_pool_time()
        item_drop_chance = self.get_item_drop_chance()

        return {
            "type": mission_type,
            "name": mission_name,
            "goal_items": goal_items,
            "pool_size": pool_size,
            "pool_time": {
                "per_item": pool_time,
                "total": total_pool_time
            },
            "item_drop_chance": item_drop_chance
        }
