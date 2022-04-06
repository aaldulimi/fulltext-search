import requests
from selectolax.parser import HTMLParser
import datetime
import asyncio
import aiohttp
from document import Document


all_days = []

base_url = 'https://www.nytimes.com/sitemap/2021/'
response = requests.get(base_url)

for node in HTMLParser(response.text).css('div > ol > li'):
    url = base_url + node.child.attrs['href']

    response = requests.get(url)
    for node in HTMLParser(response.text).css('div > ol > li'):
        day_url = url + node.child.attrs['href']
        all_days.append(day_url)

#conn = aiohttp.TCPConnector(limit=500)
print("FETCH DONE")
"""
async def fetch_articles():
    total = 0
    day = 0
    for day_url in all_days:
        day += 1
        response = requests.get(day_url)
        for node in HTMLParser(response.text).css('div > ul:nth-child(4) > li'):
            article_url = node.child.attrs['href']
            if node.child.text() == "Read the document": continue
            if article_url.find('.com/interactive') != -1 or article_url.find('books/review/') != -1: continue

            response = requests.get(article_url)
            article = HTMLParser(response.text)

            title = article.css_first('h1').text()

            # time:not(.header)
            date = article.css_first('time')
            date = date.attributes['datetime']
            if 'Z' in date: date = date[:date.find('.000Z')] + '+00:00'
            date = datetime.datetime.fromisoformat(date)
            
            author = article.css_first('span.last-byline')
            if author == None: author = 'NYTimes_staff' 
            else: author = author.child.text()

            body = ''
            for node in article.css('div.StoryBodyCompanionColumn'):
                paragraph = node.child.select('p').matches
                for p in paragraph:
                    if p: body += p.text()
                
            
            total += 1

            print(f'DAY {day:02}: {total:03}')
            


asyncio.run(fetch_articles())

"""

article_count = 0
async def get_article(session, url):
    async with session.get(url) as resp:
        article_data = await resp.text()

        if article_data:
            global article_count
            article_count += 1
            print(article_count, url)

            return 1

# 2000 in 1.15
# make getting day_url async, and make getting article_url async to o
async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for day_url in all_days: 
            response = requests.get(day_url)

            for node in HTMLParser(response.text).css('div > ul:nth-child(4) > li'):
                if node.child.text() == "Read the document": continue
                article_url = node.child.attrs['href']

                if article_url.find('.com/interactive') != -1 or article_url.find('books/review/') != -1: continue

                tasks.append(asyncio.ensure_future(get_article(session, article_url)))

        transaction_count = await asyncio.gather(*tasks)
       
        return 

asyncio.run(main())