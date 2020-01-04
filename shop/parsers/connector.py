from bs4 import BeautifulSoup


async def connect(url, session):
    async with session.get(url) as response:
        html = await response.text()
        print(f"Connect to {url}")
        return html


async def connect_2(url, session):
    async with session.get(url) as response:
        html = await response.text()
        soup = BeautifulSoup(html, 'lxml')
        print(f"Connect to {url}")
        return soup
