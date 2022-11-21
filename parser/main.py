from bs4 import BeautifulSoup
from typing import Union, List
from datetime import datetime
from crawler import DragonPageCrawler

class HTMLParser:
    def __init__(self, html:Union[str, bytes]) -> None:
        self.html = html

    def get_soup(self):
        return BeautifulSoup(self.html, "html.parser")

    def parse_html(self):
        pass

class HeroicRaceLap:
    def __init__(self, lap_soup:BeautifulSoup) -> None:
        self.lap_soup = lap_soup

    def get_lap_number(self) -> int:
        lap_and_node_numbers = self.node_soup.select_one("div.nnh").text
        lap_number = int(lap_and_node_numbers.split("-")[0].replace("Lap", ""))

        return lap_number

    def get_lap_nodes(self) -> List[dict]:
        nodes_soup = self.lap_soup.select("div.nn")

        nodes = [ HeroicRaceNode(node_soup) for node_soup in nodes_soup ]

        return nodes

    def get_all(self) -> dict:
        lap_number = self.get_lap_number()
        lap_nodes = self.get_lap_nodes()

        return {
            "number": lap_number,
            "nodes": lap_nodes
        }

class HeroicRaceNode:
    def __init__(self, node_soup:BeautifulSoup) -> None:
        self.node_soup = node_soup

    def get_node_number(self) -> int:
        lap_and_node_numbers = self.node_soup.select_one("div.nnh").text
        node_number = int(lap_and_node_numbers.split("-")[1].replace("Node", ""))
        return node_number
    
    def get_node_missions(self) -> List[dict]:
        missions_soup = self.node_soup.select("div.mm")

        missions = [ HeroicRaceMission(mission_soup).get_all() for mission_soup in missions_soup ]

        return missions

    def get_all(self) -> dict:
        node_number = self.get_node_number()
        node_missions = self.get_node_missions()

        return {
            "number": node_number,
            "missions": node_missions
        }

class HeroicRaceMission:
    def __init__(
        self,
        mission_soup:BeautifulSoup
    ) -> None:
        self.mission_soup = mission_soup

        self.info_divs = mission_soup.select("div.m2")

    def get_type(self) -> str:
        MISSON_TYPES = {
            "Collect Food": "food",
            "Battle Dragons": "battle",
            "Hatch Eggs": "hatch",
            "Feed Dragons": "feed",
            "League Battles": "pvp",
            "Collect Gold": "gold"
        }
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
    
    def __convert_pool_time_to_seconds(self, pool_time:str) -> int:
        SECONDS_PER_MINUTE = 60
        MINUTES_PER_HOUR = 60
        SECONDS_PER_HOUR = SECONDS_PER_MINUTE * MINUTES_PER_HOUR
        HORS_PER_DAY = 24
        SECONDS_PER_DAY = SECONDS_PER_HOUR * HORS_PER_DAY

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
        pool_time_seconds = self.__convert_pool_time_to_seconds(pool_time)
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

DRAGON_ELEMENTS = {
    "w": "water",
    "p": "plant",
    "f": "fire",
    "d": "dark",
    "e": "earth",
    "el": "electric",
    "m": "metal",
    "i": "ice",
    "wr": "war",
    "l": "legend",
    "li": "light",
    "pu": "pure",
    "bt": "beauty",
    "ch": "chaos",
    "mg": "magic",
    "hp": "happy",
    "dr": "dream",
    "so": "soul",
    "pr": "primal",
    "wd": "wind",
    "ti": "time"
}

DRAGON_RARITYS = {
    "c": "COMMON",
    "r": "RARE",
    "v": "VERY_RARE",
    "e": "EPIC",
    "l": "LEGENDARY",
    "h": "HEROIC"
}

class DragonPageParser:
    def __init__(self, page_url: str) -> None:
        page_html = self.__get_page_html(page_url)
        self.__page_soup = self.__get_page_soup(page_html)

    def __get_page_html(self, dragon_page_url:str) -> str:
        return DragonPageCrawler(dragon_page_url).get_html()

    def __get_page_soup(self, dragon_page_html:str) -> BeautifulSoup:
        return BeautifulSoup(dragon_page_html, "html.parser")

    def get_name(self) -> str:
        name = self.__page_soup.select_one("h1").text
        return name

    def get_rarity(self) -> str:
        rarity_img = self.__page_soup.select_one("div.img_rar")
        rarity = rarity_img.attrs["class"].split(" ")[0].split("_")[2].upper()
        return rarity

    def get_elements(self) -> List[str]:
        elements_soup = self.__page_soup.select("#typ_hull .typ_i")

        elements = []

        for element_soup in elements_soup:
            abbreviated_element_name = element_soup.attrs["class"].split(" ")[1].split("_")[1]
            elements.append(DRAGON_ELEMENTS[abbreviated_element_name])

        return elements

    def get_image_url(self) -> str:
        image_url = self.__page_soup.select_one("img.drag_img").attrs["src"].replace("../../", "https://deetlist.com/dragoncity/")
        return image_url

    def get_description(self) -> str:
        bio_soup = self.__page_soup.select_one("div#self_bio")

        description = bio_soup.text.split("\n")[2].replace("Description:", "").strip()

        return description

    def get_basic_attacks(self) -> List[dict]:
        base_attacks_soup = self.__page_soup.select("p.brtext+ div.b_split div.att_hold")

        attacks_name = [ base_attack_soup.text.split("\n")[2] for base_attack_soup in base_attacks_soup ]

        atacks_elements = [ base_attack_soup.text.split("\n")[3].split("|")[1].strip() for base_attack_soup in base_attacks_soup ]

        atacks_damege = [ base_attack_soup.text.split("\n")[3].split("|")[0].replace("Damage:", "").strip() for base_attack_soup in base_attacks_soup ]

    def get_trainable_attacks(self) -> List[dict]:
        return
    
    def get_weakness(self) -> List[str]:
        return

    def get_strengths(self) -> List[str]:
        return

    def get_book_id(self) -> int:
        return

    def get_category(self) -> int:
        return

    def get_is_breedable(self) -> bool:
        return

    def get_summon_time(self) -> int:
        return

    def get_buy_price(self) -> dict:
        return

    def get_hatch_time(self) -> int:
        return

    def get_hatch_xp(self) -> int:
        return

    def get_release_date(self) -> int:
        return

    def get_sell_price(self) -> int:
        return  

    def get_starting_income_of_gold(self) -> int:
        return

    def get_all(self) -> dict:
        return {}

class HeroicRaceParser(HTMLParser):
    def __init__(self, html:Union[str, bytes]) -> None:
        super().__init__(html)

        self.__island_soup = super().get_soup()

    def get_island_duration(self) -> int:
        island_duration_txt = self.__island_soup.select_one("div.dur_text").text
        island_duration = int(island_duration_txt.replace("This event lasts", "").replace("days", ""))
        return island_duration

    def get_dragons(self) -> List[dict]:
        dragons_soup = self.__island_soup.select("div.over")

        dragons_page_url = [ 
            dragon_soup.select_one("a").attrs["href"].replace("../../", "https://deetlist.com/")
            for dragon_soup in dragons_soup 
        ]
        
        dragons = [ DragonPageParser(dragon_page_url).get_all() for dragon_page_url in dragons_page_url ]

        return dragons

    def get_laps(self) -> List[dict]:
        laps_soup = self.__island_soup.select("div.hl")
        
        laps = [ HeroicRaceLap(lap_soup).get_all() for lap_soup in laps_soup ]

        return laps

    def get_all(self) -> dict:
        island_duration = self.get_island_duration()
        island_dragons = self.get_dragons()
        island_laps = self.get_laps()

        return {
            "duration": island_duration,
            "dragons": island_dragons,
            "laps": island_laps
        }