from bs4 import BeautifulSoup

class AllDragonsParser:
    def __init__(self, html):
        self.__soup = BeautifulSoup(html, "html.parser")

    def get_names(self) -> list[str]:
        return [ dragon_soup.text.strip() for dragon_soup in self.__soup.select("a:has(.drag)") ]

    def get_page_urls(self) -> list[str]:
        return [ 
            dragon_soup.attrs["href"].replace("../", "https://deetlist.com/dragoncity/").replace(" ", "%20")
            for dragon_soup in self.__soup.select("a:has(.drag)")
        ]

    def get_img_urls(self) -> list[str]:
        return [ 
            dragon_soup.attrs["href"].replace("../", "https://deetlist.com/dragoncity/img/").replace(" ", "%20").lower() + ".png"
            for dragon_soup in self.__soup.select("a:has(.drag)")
        ]

    def get_all(self) -> list[dict]:
        pass
