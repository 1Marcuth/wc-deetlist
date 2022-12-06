from typing import List, Union
from bs4 import BeautifulSoup

from .lap import LapParser
from ....config import SECONDS_PER_DAY

class HeroicRaceParser:
    def __init__(self, html: Union[str, bytes]) -> None:
        self.__island_soup = BeautifulSoup(html, "html.parser")

    def get_island_duration(self) -> int:
        island_duration_txt = self.__island_soup.select_one("div.dur_text").text
        island_duration = int(island_duration_txt.strip().removeprefix("This event lasts").removesuffix("days")) * SECONDS_PER_DAY
        return island_duration

    def get_dragon_page_urls(self) -> List[dict]:
        dragons_soup = self.__island_soup.select("div.over")

        dragon_page_urls = [ 
            dragon_soup.select_one("a").attrs["href"].replace("../../", "https://deetlist.com/dragoncity/")
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