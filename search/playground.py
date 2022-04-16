import requests
from selectolax.parser import HTMLParser
import datetime

header = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Mobile Safari/537.36'
}
response = requests.get('https://www.nytimes.com/2022/04/15/world/europe/ukraine-russia-occupation.html', headers=header)
#print(response.text)
article = HTMLParser(response.text)

title = article.css_first('h1')
author = article.css_first('span.last-byline')
if author == None: author = 'unkown' 
else: author = author.child.text()

date = article.css_first('time')
date = date.attributes['datetime']
if 'Z' in date: date = date[:date.find('.000Z')] + '+00:00'
date = datetime.datetime.fromisoformat(date)



print(date.strftime('%Y-%m-%d %H:%M:%S'))
