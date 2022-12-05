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
        dragon_infos = []

        names = self.get_names()
        page_urls = self.get_page_urls()
        img_urls = self.get_img_urls()

        for name, page_url, img_url in zip(names, page_urls, img_urls):
            dragon_info = {
                "name": name,
                "page_url": page_url,
                "img_url": img_url
            }

            dragon_infos.append(dragon_info)
        
        return dragon_infos