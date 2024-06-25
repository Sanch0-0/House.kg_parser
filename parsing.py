import aiohttp
from typing import AsyncGenerator
from bs4 import BeautifulSoup as BS # type: ignore

async def send_request(url: str) -> str | None:

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()

            return None


async def get_links(html: str) -> AsyncGenerator[str, str]:
    soup = BS(markup=html, features="html.parser")

    listings: list[BS] = soup.find("div", class_="listings-wrapper").find_all("div", class_="listing")

    for listing in listings:
        domen = "https://www.house.kg"
        url = listing.find("a").get("href")

        yield domen + url


async def parse_page(html: str) -> dict[str, str | None]:
    soup = BS(markup=html, features="html.parser")

    header = soup.find("div", class_="details-header")

    title = header.find("div", class_="left").find("h1").text.strip()
    address = header.find("div", class_="left").find("div", class_="address").text.strip()

    price_usd = header.find("div", class_="right").find("div", class_="price-dollar").text.strip()
    price_som = header.find("div", class_="right").find("div", class_="price-som").text.strip()

    added = header.find("div", class_="bottom-info").find("span", class_="added-span").text.strip()

    data = {
        "title": title,
        "address": address,
        "price_usd": price_usd,
        "price_som": price_som,
        "added": added
    }
    return data
