import json

import requests

from config import USER_ID, RCJar, headers, proxies
from db import DbClient

index_url = f"https://www.pixiv.net/ajax/user/{USER_ID}/illusts/bookmarks"
db = DbClient()


def scrape_index(offset=0, limit=48, rest="show", lang="zh"):
    url = f"{index_url}?tag=&offset={offset}&limit={limit}&rest={rest}&lang={lang}"
    rsp = requests.get(url, cookies=RCJar, headers=headers, proxies=proxies)
    return rsp.json()


def parse_data(data):
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


def scrape_data(pids):
    url = "https://www.pixiv.net/ajax/illust/{}"
    err_cnt = 0
    for pid in pids:
        if err_cnt > 10:
            break
        rsp = requests.get(url.format(pid), cookies=RCJar, headers=headers, proxies=proxies).json()
        if rsp["error"]:
            print(rsp["message"])
            err_cnt += 1
        parse_data(rsp["body"])


def run():
    err_cnt = 0
    for i in range(0, 1000, 48):
        if err_cnt > 10:
            break
        index = scrape_index(offset=i)
        if index["error"]:
            print(index["message"])
            err_cnt += 1
        scrape_data([item["id"] for item in index["body"]["works"]])


if __name__ == '__main__':
    run()
