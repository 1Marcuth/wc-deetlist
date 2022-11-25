from bs4 import BeautifulSoup
from typing import Union, List
from datetime import datetime

from ...config import (
    MINUTES_PER_HOUR,
    SECONDS_PER_DAY,
    SECONDS_PER_HOUR,
    SECONDS_PER_MINUTE
)

MISSON_TYPES = {
    "Collect Food": "food",
    "Battle Dragons": "battle",
    "Hatch Eggs": "hatch",
    "Feed Dragons": "feed",
    "League Battles": "pvp",
    "Collect Gold": "gold"
}

class HeroicRaceParser:
    def __init__(self, html: Union[str, bytes]) -> None:
        self.__island_soup = BeautifulSoup(html, "html.parser")

    def get_island_duration(self) -> int:
        island_duration_txt = self.__island_soup.select_one("div.dur_text").text
        island_duration = int(island_duration_txt.replace("This event lasts", "").replace("days", ""))
        return island_duration

    def get_dragon_page_urls(self) -> List[dict]:
        dragons_soup = self.__island_soup.select("div.over")

        dragon_page_urls = [ 
            dragon_soup.select_one("a").attrs["href"].replace("../../", "https://deetlist.com/")
            for dragon_soup in dragons_soup 
        ]

        return dragon_page_urls

    def get_laps(self) -> List[dict]:
        laps_soup = self.__island_soup.select("div.hl")
        
        laps = [ LapParser(lap_soup).get_all() for lap_soup in laps_soup ]

        return laps

    def get_all(self) -> dict:
        island_duration = self.get_island_duration()
        island_dragon_page_urls = self.get_dragon_page_urls()
        island_laps = self.get_laps()

        return {
            "duration": island_duration,
            "dragon_page_urls": island_dragon_page_urls,
            "laps": island_laps
        }

class LapParser:
    def __init__(self, lap_soup: BeautifulSoup) -> None:
        self.lap_soup = lap_soup

    def get_lap_number(self) -> int:
        lap_and_node_numbers = self.lap_soup.select_one("div.nnh").text
        lap_number = int(lap_and_node_numbers.split("-")[0].replace("Lap", ""))

        return lap_number

    def get_lap_nodes(self) -> List[dict]:
        nodes_soup = self.lap_soup.select("div.nn")

        nodes = [ NodeParser(node_soup) for node_soup in nodes_soup ]

        return nodes

    def get_all(self) -> dict:
        lap_number = self.get_lap_number()
        lap_nodes = self.get_lap_nodes()

        return {
            "number": lap_number,
            "nodes": lap_nodes
        }

class NodeParser:
    def __init__(self, node_soup:BeautifulSoup) -> None:
        self.node_soup = node_soup

    def get_node_number(self) -> int:
        lap_and_node_numbers = self.node_soup.select_one("div.nnh").text
        node_number = int(lap_and_node_numbers.split("-")[1].replace("Node", ""))
        return node_number
    
    def get_node_missions(self) -> List[dict]:
        missions_soup = self.node_soup.select("div.mm")

        missions = [ MissionParser(mission_soup).get_all() for mission_soup in missions_soup ]

        return missions

    def get_all(self) -> dict:
        node_number = self.get_node_number()
        node_missions = self.get_node_missions()

        return {
            "number": node_number,
            "missions": node_missions
        }

class MissionParser:
    def __init__(
        self,
        mission_soup:BeautifulSoup
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
    
    def __pool_time_to_seconds(self, pool_time:str) -> int:
        pool_time = pool_time.lower()

        if pool_time == "instant" or pool_time == "no minimum":
            return 0
        
        if "minutes" in pool_time:
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
  
    def get_pool_time(self) -> int:
        pool_time = self.info_divs[2].text
        pool_time_seconds = self.__pool_time_to_seconds(pool_time)
        return pool_time_seconds

    def get_item_drop_chance(self) -> str:
        drop_chance = self.info_divs[3].text
        return drop_chance

    def get_total_pool_time(self) -> int:
        total_pool_time = self.info_divs[4].text
        total_pool_time_seconds = self.__convert_pool_time_to_seconds(total_pool_time)
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

