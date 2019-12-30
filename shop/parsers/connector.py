from bs4 import BeautifulSoup

HEADERS = {'User-Agent': 'Mozilla/5.0'}


async def connect(url, session):
    print(f"Connect to {url}")
    async with session.get(url, headers=HEADERS) as response:
        html = await response.text()
        soup = BeautifulSoup(html, "html.parser")
        return soup
