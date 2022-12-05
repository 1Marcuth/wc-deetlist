from ..crawler import (
    AllDragonsCrawler,
    DragonPageCrawler,
    HeroicRacesCrawler
)
from ..parser import (
    AllDragonsParser,
    DragonPageParser,
    HeroicRaceParser
)

def get_dragon_full_data(page_url: str):
    html = DragonPageCrawler(page_url).get_html()
    data = DragonPageParser(html).get_all()

    return data

def get_all_dragons_full_data():
    html = AllDragonsCrawler().get_html()
    raw_dragons = AllDragonsParser(html).get_all()

    dragons = []

    for raw_dragon in raw_dragons:
        dragon = get_dragon_full_data(raw_dragon["page_url"])
        print(dragon["book_id"])

        dragons.append(dragon)

    return dragons

def get_heroic_race_data():
    html = HeroicRacesCrawler().get_html()
    data = HeroicRaceParser(html).get_all()

    return data

def get_heroic_race_full_data():
    raw_data = get_heroic_race_data()

    dragons = []

    for dragon_page_url in raw_data["dragon_page_urls"]:
        dragon = get_dragon_full_data(dragon_page_url)

        dragons.append(dragon)

    data = raw_data.copy()

    data.pop("dragon_page_urls")

    data["dragons"] = dragons

    return data

