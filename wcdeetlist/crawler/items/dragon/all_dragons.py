from ...crawler import WebCrawler

class AllDragonsCrawler(WebCrawler):
    __url = "https://deetlist.com/dragoncity/all-dragons/"

    def __init__(self):
        super().__init__(self.__url)
