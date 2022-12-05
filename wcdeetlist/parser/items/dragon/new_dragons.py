from bs4 import BeautifulSoup

class NewDragonsParser:
    def __init__(self, html: str):
        self.__page_soup = BeautifulSoup(html, "html.parser")

    def get_names(self) -> list[str]:
        return

    def get_raritys(self) -> lsit[str]:
        return