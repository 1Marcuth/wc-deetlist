from ..crawler import WebCrawler

class HeroicRaceCrawler(WebCrawler):
    __url = "https://deetlist.com/dragoncity/events/race/"

    def __init__(
        self,
    ) -> None:
        super().__init__(self.__url)
