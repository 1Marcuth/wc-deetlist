from typing import List
from bs4 import BeautifulSoup

from .mission import MissionParser

class NodeParser:
    def __init__(self, node_soup: BeautifulSoup) -> None:
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