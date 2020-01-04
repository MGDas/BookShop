import asyncio
import aiohttp
from bs4 import BeautifulSoup

from shop.parsers.connector import connect_2
from shop.parsers.get_genre import CATALOG_URL
from shop.models import Genre, Book


def save_db(name, photo_url=None, genre=None):

    try:
        genre = Genre.objects.get(name=genre)
    except:
        genre = None

    book, status = Book.objects.get_or_create(name=name, genre=genre, photo_url=photo_url)

    if status:
        print(f"{book} ........ SAVE .. id={book.id}")
    else:
        print(f"{book} ........ ALREADY .. id={book.id}")


async def get_genres():

    genres = Genre.objects.filter(children__isnull=True)

    tasks = []
    async with aiohttp.ClientSession() as session:
        for genre in genres:
            url = f"{CATALOG_URL}/{genre.slug}"
            task = asyncio.create_task(connect_2(url, session))
            tasks.append(task)

        return await asyncio.gather(*tasks)


async def get_book_data():

    soups = await get_genres()

    for soup in soups:
        try:
            genre = soup.find_all('div', class_='breadcrumbs__item')
        except:
            genre = None

        if genre:
            genre_name = genre[-1].text

        try:
            books = soup.find_all("div", class_="catalog-products__item") # div .catalog-products__item
        except:
            continue

        for book in books:
            name = book.find("div", class_="book__title").text.strip()

            try:
                photo_url = book.find_all("source")[1]['data-srcset'].split(" ")[0]
            except:
                photo_url = None

            save_db(name=name, genre=genre_name, photo_url=photo_url)


def main():
    asyncio.run(get_book_data())
