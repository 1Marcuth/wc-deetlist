from ...crawler import WebCrawler

class NewDragonsCrawler(WebCrawler):
    __url = "https://deetlist.com/dragoncity/new-dragons/"

    def __init__(self):
        super().__init__(self.__url)
