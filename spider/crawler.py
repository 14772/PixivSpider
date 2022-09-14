import asyncio
import json
import logging

import aiohttp

from config import USER_ID, headers, proxy
from cookie import get_cookie
from db import DbClient

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

CONCURRENCY = 5

session = None
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

INDEX_URL = f"https://www.pixiv.net/ajax/user/{USER_ID}/illusts/bookmarks"
db = DbClient()


async def base_scrape(url: str) -> dict:
    """
    封装请求\n
    :param url: 目标url
    :return: json格式数据
    """
    async with asyncio.Semaphore(CONCURRENCY):
        try:
            async with session.get(url, headers=headers, proxy=proxy) as rsp:
                return await rsp.json()
        except aiohttp.ClientError:
            logging.error(f'scraping {url} failed', exc_info=True)


async def scrape_index(offset: int = 0, limit: int = 48, rest: str = "show", lang: str = "zh") -> dict:
    """
    爬取收藏夹\n
    :param offset: 偏移量
    :param limit: 限制数量
    :param rest: show or hide
    :param lang: zh or en
    :return: json格式数据
    """
    url = f"{INDEX_URL}?tag=&offset={offset}&limit={limit}&rest={rest}&lang={lang}"
    return await base_scrape(url)


async def parse_data(data: dict):
    """
    解析数据，调用db存储\n
    :param data: 数据
    """
    pid = data["id"]
    title = data["title"]
    urls = data["urls"]
    tags = []
    for tag in data["tags"]["tags"]:
        tags.append(tag["tag"])
        tags.append(tag["translation"]["en"]) if tag.get("translation", None) else None
    uid = data["userId"]
    author = data["userName"]
    width = data["width"]
    height = data["height"]
    page_count = data["pageCount"]
    r18 = 1 if data["xRestrict"] else 0
    db.insert((pid, title, json.dumps(urls), ' '.join(tags), uid, author, width, height, page_count, r18))
    logging.info(f"insert {pid} into db")


async def scrape_data(pids: list[int]):
    """
    爬取图片数据\n
    :param pids: pid列表
    """
    for pid in pids:
        if db.query(pid):
            logging.info(f"{pid} already exists")
            continue
        rsp = await base_scrape(f"https://www.pixiv.net/ajax/illust/{pid}")
        if rsp["error"]:
            logging.error(rsp["message"])
            continue
        await parse_data(rsp["body"])


async def main(start: int):
    """
    主函数\n
    每次请求144个，避免短时间内请求过多\n
    :param start: 起始值
    """
    global session
    session = aiohttp.ClientSession(cookies=get_cookie(), trust_env=True)
    scrape_index_tasks = [asyncio.ensure_future(scrape_index(offset)) for offset in range(start, start + 144, 48)]
    results = await asyncio.gather(*scrape_index_tasks)
    ids = []
    for result in results:
        if result["error"]:
            logging.error(result["message"])
            continue
        for data in result["body"]["works"]:
            ids.append(data["id"])
    scrape_data_tasks = [asyncio.ensure_future(scrape_data(ids[i:i + 10])) for i in range(0, len(ids), 10)]
    await asyncio.wait(scrape_data_tasks)
    await session.close()


if __name__ == '__main__':
    asyncio.run(main(432))
