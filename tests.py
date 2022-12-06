from wcdeetlist.crawler import NewDragonsCrawler
from wcdeetlist.parser import NewDragonsParser

html = NewDragonsCrawler().get_html()
data = NewDragonsParser(html).get_all()

print(data)