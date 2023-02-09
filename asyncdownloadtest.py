
STATISTICS_URL = 'https://www.appsloveworld.com/wp-content/uploads/2018/10/640.mp4'#'https://www.python.org/ftp/python/3.5.1/python-3.5.1-embed-win32.zip'

import time
import os
import os.path
from bs4 import BeautifulSoup as bs
import aiohttp
import aiofiles
import asyncio
import urllib
import typing


#STATISTICS_URL = 'https://digital.nhs.uk/data-and-information/publications/statistical/mental-health-services-monthly-statistics'
OUTPUT_FOLDER = 'video/'


async def fetch_download_links(session: aiohttp.ClientSession, url: str) -> typing.List[str]:
    r = await session.get(url, ssl=False)
    soup = bs(await r.text(), 'lxml')
    link = 'https://digital.nhs.uk' + soup.select_one('.cta__button')['href']

    r = await session.get(link, ssl=False)
    soup = bs(await r.text(), 'lxml')
    return [i['href'] for i in soup.select('.attachment a')]


async def place_file(session: aiohttp.ClientSession, source: str) -> None:
    r = await session.get(source, ssl=False)

    file_name = urllib.parse.unquote(source.split('/')[-1])
    async with aiofiles.open(os.path.join(OUTPUT_FOLDER, file_name), 'wb') as f:
        async for data in r.content.iter_any():
            await f.write(data)


async def main():
    async with aiohttp.ClientSession() as session:
        #urls = await fetch_download_links(session, STATISTICS_URL)
        urls = [STATISTICS_URL]
        await asyncio.gather(*[place_file(session, url) for url in urls])


if __name__ == '__main__':
    t1 = time.perf_counter()
    print('process started...')
    asyncio.get_event_loop().run_until_complete(main())
    #os.startfile(OUTPUT_FOLDER[:-1])
    t2 = time.perf_counter()
    print(f'Completed in {t2-t1} seconds.')
