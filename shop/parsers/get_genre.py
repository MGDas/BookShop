import aiohttp
import asyncio
from bs4 import BeautifulSoup

from shop.parsers.connector import connect
from shop.models import Genre


BASE_URL = "https://book24.ru"
CATALOG_URL = "https://book24.ru/catalog"

genres_list = ['Сувениры. Аксессуары', 'Канцтовары', 'Хобби и творчество',
                'Игры и игрушки', 'Книжный развал', 'Календари 2020', 'Детская литература']

def save_db(name, slug, parent=None):

    try:
        parent = Genre.objects.get(name=parent)
    except:
        parent = None

    genre, status = Genre.objects.get_or_create(name=name, slug=slug, parent=parent)

    if status:
        print(f"{genre} ........ SAVE .. id={genre.id}")
    else:
        print(f"{genre} ........ ALREADY .. id={genre.id}")


async def get_url_sub_genre(url, session):

    html = await connect(url, session)
    soup = BeautifulSoup(html, 'lxml')

    breads = soup.find_all('div', class_='breadcrumbs__item')
    genres = soup.find('div', class_='catalog-filter__category').find_all('a', class_='filter-item__link')

    for genre in genres:
        genre.span.decompose()
        name = genre.text.strip()

        if name in genres_list:
            return

        link = genre['href']
        slug = link.split('/')[-2]

        if len(breads) < 3:
            parent = None
        else:
            parent = breads[-1].text

        save_db(name, slug, parent)
        genres_list.append(name)

        await get_url_sub_genre(BASE_URL + link, session)


async def get_data():
    async with aiohttp.ClientSession() as session:
        return await get_url_sub_genre(CATALOG_URL, session)


def main():
    asyncio.run(get_data())
