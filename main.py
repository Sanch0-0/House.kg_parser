import time

import asyncio
from parsing import send_request, get_links, parse_page


async def fetch_and_parse(url: str) -> dict[str, str | None] | None:
    html = await send_request(url=url)

    if html is not None:
        data = await parse_page(html=html)
        return data
    else:
        return None


async def main() -> None:
    url = "https://www.house.kg/snyat-kvartiru?rooms=1&sort_by=upped_at%20desc&page=1"

    html = await send_request(url)

    if html is None:
        print("Запрос не удался!")
        return None

    tasks = []
    async for url in get_links(html=html):
        tasks.append(fetch_and_parse(url=url))

    print(await asyncio.gather(*tasks))


if __name__ == "__main__":
    asyncio.run(main())
