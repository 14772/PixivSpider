import json

from requests.cookies import RequestsCookieJar

USER_ID = 45087890

with open("pixiv_cookie", "r", encoding="utf8") as fp:
    cookies = json.load(fp)
    RCJar = RequestsCookieJar()
    for cookie in cookies:
        RCJar.set(cookie['name'], cookie['value'])

headers = {
    "Host": "www.pixiv.net",
    "referer": "https://www.pixiv.net/",
    "origin": "https://accounts.pixiv.net",
    "accept-language": "zh-CN,zh;q=0.9",
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 '
                  'Safari/537.36',
}
proxies = {
    "http": "socks5://127.0.0.1:10808",
    "https": "socks5://127.0.0.1:10808"
}
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "sukun031015",
    "database": "pixiv",
    "charset": "utf8mb4"
}
