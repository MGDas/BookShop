import asyncio
import aiohttp
import re
from bs4 import BeautifulSoup as bs
from shop.models import Genre
from shop.parsers.connector import connect


base_url = "https://www.spbdk.ru"
link = "https://www.spbdk.ru/catalog/knigi/khudozhestvennaya_literatura/detektiv/"


async def get_soup():

    tasks = []
    async with aiohttp.ClientSession() as session:
        for num in range(0, 20):
            task = asyncio.create_task(connect(link + f"?PAGEN_2={num}", session))
            tasks.append(task)

        return await asyncio.gather(*tasks)


def pars_page_with_books(soups):
    urls = []
    print(len(soups), "pars_page_with_books")
    for soup in soups:
        for s in soup.select(".snippet__content .snippet__title"):
            print(s.text)
            urls.append(base_url + s['href'])

    return urls


async def get_data():

    soups = await get_soup()
    urls = pars_page_with_books(soups)

    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            print(f"get_data url={url}")
            task = asyncio.create_task(connect(url, session))
            tasks.append(task)

        return await asyncio.gather(*tasks)


async def book_page():

    soups = await get_data()

    for soup in soups:
        name = soup.select_one(".title.h1").text
        print(name)


def main():
    asyncio.run(book_page())
