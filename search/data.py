import requests
from selectolax.parser import HTMLParser
import datetime
import asyncio
import aiohttp
from document import Document
import random
import xml.dom.minidom
import xml.etree.ElementTree as ET


ARTICLE_LIMIT = 100

headers = {
    'user-agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.{random.randint(0, 9999)} Safari/537.{random.randint(0, 99)}'  
}

all_days = []

base_url = 'https://www.nytimes.com/sitemap/2021/'
response = requests.get(base_url, headers=headers)

for node in HTMLParser(response.text).css('div > ol > li'):
    url = base_url + node.child.attrs['href']

    response = requests.get(url)
    for node in HTMLParser(response.text).css('div > ol > li'):
        day_url = url + node.child.attrs['href']
        all_days.append(day_url)

print('FETCH IS DONE')

article_count = 0
async def get_article_data(session, url):
    async with session.get(url) as resp:
        response_text = await resp.text()
        
        if response_text:            
            article = HTMLParser(response_text)

            title = article.css_first('h1').text()

            date = article.css_first('time')
            date = date.attributes['datetime']
            if 'Z' in date: date = date[:date.find('.000Z')] + '+00:00'
            date = datetime.datetime.fromisoformat(date)
            date = date.strftime('%Y-%m-%d %H:%M:%S')

            author = article.css_first('span.last-byline')
            if author == None: author = 'unkown' 
            else: author = author.child.text()

            body = ''
            for node in article.css('div.StoryBodyCompanionColumn'):
                paragraph = node.child.select('p').matches
                for p in paragraph:
                    if p: body += p.text()

            
            doc = ET.Element('doc')
            ET.SubElement(doc, "title").text = title
            ET.SubElement(doc, "body").text = body
            ET.SubElement(doc, "author").text = author
            ET.SubElement(doc, "datetime").text = date
            ET.SubElement(doc, "url").text = url

            dom = xml.dom.minidom.parseString(ET.tostring(doc))
            xml_string = dom.toprettyxml()
            
            part1, part2 = xml_string.split('?>')
            print(part2)

            with open("data.xml", 'a') as file:
                file.write(part2)
                file.close()


            # print(article_count, title)

        return 

async def get_article_url(session, url):
    async with session.get(url) as resp:
        day_data = await resp.text()

        all_articles = []
        for node in HTMLParser(day_data).css('div > ul:nth-child(4) > li'):
            if node.child.text() == "Read the document": continue
            article_url = node.child.attrs['href']
            if article_url.find('.com/interactive') != -1 or article_url.find('books/review/') != -1: continue
            
            global article_count

            if article_count < ARTICLE_LIMIT: 
                article_count += 1
                all_articles.append(asyncio.ensure_future(get_article_data(session, article_url)))


        collection = await asyncio.gather(*all_articles)

         

async def main():
    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = []
        for day_url in all_days: 
            tasks.append(asyncio.ensure_future(get_article_url(session, day_url)))
        
        collection = await asyncio.gather(*tasks)


asyncio.run(main())
