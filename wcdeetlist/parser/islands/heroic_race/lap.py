from typing import List
from bs4 import BeautifulSoup

from .node import NodeParser

class LapParser:
    def __init__(self, lap_soup: BeautifulSoup) -> None:
        self.lap_soup = lap_soup

    def get_lap_number(self) -> int:
        lap_and_node_numbers = self.lap_soup.select_one("div.nnh").text
        lap_number = int(lap_and_node_numbers.split("-")[0].replace("Lap", ""))

        return lap_number

    def get_lap_nodes(self) -> List[dict]:
        nodes_soup = self.lap_soup.select("div.nn")

        nodes = [ NodeParser(node_soup).get_all() for node_soup in nodes_soup ]

        return nodes

    def get_all(self) -> dict:
        lap_number = self.get_lap_number()
        lap_nodes = self.get_lap_nodes()

        return {
            "number": lap_number,
            "nodes": lap_nodes
        }