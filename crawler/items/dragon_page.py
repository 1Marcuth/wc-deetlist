from ..crawler import WebCrawler

class DragonPageCrawler(WebCrawler):
    def __init__(self, url:str) -> None:
        super().__init__(url)

    def get_html(self) -> str:
        return super().get_html()