from wcdeetlist.crawler import NewDragonsCrawler
from wcdeetlist.parser import NewDragonsParser
import json

html = NewDragonsCrawler().get_html()
data = NewDragonsParser(html).get_all()

print(json.dumps(data, indent=4))