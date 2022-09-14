import json
import logging
import random

from flask import Flask, request, jsonify

from data_source import DbClient

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_MIMETYPE'] = 'application/json; charset=utf-8'
db = DbClient()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')


@app.route('/setu/random', methods=['GET'])
def random_info():
    try:
        num = request.args.get('num', 1, type=int)
        if num > 10:
            num = 10
        tags = request.args.getlist('tag')  # ["萝莉|少女", "白丝|黑丝"]
        r18 = request.args.get('r18', 2, type=int)  # 0: non-r18, 1: r18, 2: all
        proxy = request.args.get('proxy', 1, type=int)  # 0: no proxy, 1: use proxy
        sql = 'SELECT * FROM collect WHERE 1 = 1 '
        if tags:
            sql += 'AND '
            for tag in tags:
                sql += '(' + ' OR '.join([f"tags LIKE '%{t}%'" for t in tag.split('|')]) + ') AND '
            sql = sql[:-5] + ' '
        if r18 in (0, 1):
            if tags:
                sql += f"AND r18 = {r18} "
            else:
                sql += f"r18 = {r18} "
        sql += f"LIMIT 10"
        logging.info(sql)
        res = db.query(sql)
        if num <= len(res):
            res = random.sample(res, num)
        data = []
        for item in res:
            urls = json.loads(item[3])
            if proxy:
                for i in urls:
                    urls[i] = urls[i].replace('i.pximg.net', 'i.pixiv.re')
            data.append({
                'pid': item[1],
                'title': item[2],
                'urls': urls,
                'tag': item[4],
                'uid': item[5],
                'author': item[6],
                'width': item[7],
                'height': item[8],
                'page_count': item[9],
                'r18': item[10]
            })
        return jsonify({'error': False, 'msg': '', 'data': data})
    except Exception as e:
        logging.error(e)
        return jsonify({'error': True, 'msg': str(e), 'data': []})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
