from bs4 import BeautifulSoup
from datetime import datetime

from ....config import SECONDS_PER_DAY

class NewDragonsParser:
    def __init__(self, html: str):
        self.__page_soup = BeautifulSoup(html, "html.parser")

    def get_names(self) -> list[str]:
        return [ name.text for name in self.__page_soup.select(".rn") ]

    def get_released_at(self) -> list[int]:
        return [ int(time.text) for time in self.__page_soup.select(".rt") ]

    def get_raritys(self) -> list[str]:
        return [ rarity.attrs["class"][0].removeprefix("img_rp_").upper() for rarity in  self.__page_soup.select(".img_rar") ]

    def get_img_urls(self) -> list[str]:
        imgs = self.__page_soup.select(".newi")

        img_urls = []

        for img in imgs:
            img_url = img.attrs["src"].replace("../", "https://deetlist.com/dragoncity/").replace(" ", "%20")

            img_urls.append(img_url)

        return img_urls

    def get_all(self):
        return {
            "names": self.get_names(),
            "relansed_at": self.get_released_at(),
            "img_urls": self.get_img_urls(),
            "raritys": self.get_raritys()
        }