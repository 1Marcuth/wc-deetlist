# from wcdeetlist.crawler import DragonPageCrawler
# from wcdeetlist.parser import DragonPageParser

# html = DragonPageCrawler("https://deetlist.com/dragoncity/dragon/Bone").get_html()
# data = DragonPageParser(html).get_all()

# print(data)

from wcdeetlist.crawler import AllDragonsCrawler
from wcdeetlist.parser import AllDragonsParser
