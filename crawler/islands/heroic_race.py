from ..crawler import WebCrawler

class HeroicRacesCrawler(WebCrawler):
    url = "https://deetlist.com/dragoncity/events/race/"

    def __init__(
        self,
    ) -> None:
        super().__init__(self.url)

    def get_html(self) -> str:
        return super().get_html()