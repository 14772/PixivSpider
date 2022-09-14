# PixivSpider

Pixiv爬虫，爬取个人收藏，保存至数据库

技术栈：aiohttp 异步爬虫，DBUtils + PyMysql 数据库管理，Flask Web 框架，Nginx 反向代理（非必需），Docker 容器化技术。

nginx 配置文件使用 digitalocean/nginxconfig.io 生成，注意修改。

## 数据库

| 字段         | 数据类型         | 约束                         | 注释             |
|------------|--------------|----------------------------|----------------|
| id         | INT          | PRIMARY KEY AUTO_INCREMENT | 自增ID           |
| pid        | INT          | NOT NULL                   | pid            |
| title      | VARCHAR(50)  | NOT NULL                   | 标题             |
| urls       | VARCHAR(600) | NOT NULL                   | 图片地址字典,json序列化 |
| tags       | VARCHAR(300) | NOT NULL                   | 标签,含翻译         |
| uid        | INT          | NOT NULL                   | uid            |
| author     | VARCHAR(20)  | NOT NULL                   | 作者             |
| width      | INT          | NOT NULL                   | 宽度             |
| height     | INT          | NOT NULL                   | 高度             |
| page_count | INT          | NOT NULL                   | 作品所在页数         |
| r18        | INT          | NOT NULL                   | r18-1,非r18-0   |

## spider

### 部署

`config.py`中配置信息

```python
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
```

首先运行`cookie.py`，保存`pixiv_cookie`

然后启动数据库，运行`crawler.py`

## API

### 部署

`data_source`中配置数据库信息

运行：

1. 直接运行：`python3 server.py`
2. Docker 部署：`docker-compose up`

### 接口

#### 随机获取色图

##### 请求

```http
GET /setu/random
```

| 查询参数  | 参数类型     | 是否必需 | 默认值  | 说明                                                 |
|-------|----------|------|------|----------------------------------------------------|
| tag   | string[] | 否    | None | 指定标签，见下文                                           |
| num   | integer  | 否    | 1    | 一次返回的结果数量，范围为`1`到`10`。在指定关键字或标签的情况下，结果数量可能会不足指定的数量 |
| r18   | integer  | 否    | 2    | `0`为非 R18，`1`为 R18，`2`为混合（在库中的分类，不等同于作品本身的 R18 标识） |
| proxy | integer  | 否    | 1    | `0`不使用图片地址反代服务，`1`使用`i.pixiv.re`反代                 |

###### tag

按照 AND 和 OR 规则来匹配标签，使用`LIKE`关键字实现

每个字符串可以是若干个由`|`分隔的标签，它们之间应用 OR 规则

举个例子，我需要查找 **少女** 的 **白丝** 或 **黑丝** 的色图，即 **少女** AND (**白丝** OR **黑丝**)，那么可以这样发送请求

```http
GET /setu/random?tag=少女&tag=白丝|黑丝
```

###### proxy

由于 P 站资源域名`i.pximg.net`具有防盗链措施，不含`www.pixiv.net` `referrer` 的请求均会 403，所以如果需要直接在网页上展示或在客户端上直接下载必须依靠反代服务。

##### 响应

成功：200

```json
{
    "data": [
        {
            "author": "叁伞",
            "height": 1726,
            "page_count": 1,
            "pid": 100532539,
            "r18": 0,
            "tag": "熊野(アズールレーン) 熊野（碧蓝航线） おっぱい 欧派 アズールレーン 碧蓝航线 アズールレーン5000users入り 碧蓝航线5000收藏 アズレン5周年イラコン 碧蓝航线5周年插画比赛 尻神様 尻神样 饅頭(アズールレーン) 蛮啾（碧蓝航线） ふともも 大腿 ペディキュア 美甲（脚趾） 一夜千夜の願い",
            "title": "熊野",
            "uid": 5465660,
            "urls": {
                "mini": "https://i.pixiv.re/c/48x48/img-master/img/2022/08/16/18/51/34/100532539_p0_square1200.jpg",
                "original": "https://i.pixiv.re/img-original/img/2022/08/16/18/51/34/100532539_p0.jpg",
                "regular": "https://i.pixiv.re/img-master/img/2022/08/16/18/51/34/100532539_p0_master1200.jpg",
                "small": "https://i.pixiv.re/c/540x540_70/img-master/img/2022/08/16/18/51/34/100532539_p0_master1200.jpg",
                "thumb": "https://i.pixiv.re/c/250x250_80_a2/img-master/img/2022/08/16/18/51/34/100532539_p0_square1200.jpg"
            },
            "width": 1350
        }
    ],
    "error": false,
    "msg": ""
}
```