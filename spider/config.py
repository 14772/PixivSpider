USER_ID = ...  # 账户UID
USER_DIR = ...  # Chrome浏览器用户数据目录，示例r'C:\Users\Admin\AppData\Local\Google\Chrome\User Data'

headers = {
    "Host": "www.pixiv.net",
    "referer": "https://www.pixiv.net/",
    "origin": "https://accounts.pixiv.net",
    "accept-language": "zh-CN,zh;q=0.9",
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 '
                  'Safari/537.36',
}
proxy = ...  # 示例"http://127.0.0.1:1080"
db_config = {
    "host": ...,
    "user": ...,
    "password": ...,
    "database": ...,
    "charset": "utf8mb4"
}