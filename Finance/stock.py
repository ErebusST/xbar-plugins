#!/usr/bin/env python3

import datetime
import json
import time

import requests

market = 1  # 上证：1 沪市：0 北证：0
stock = "515050"


def is_time_between(start_time, end_time, check_time):
    return start_time <= check_time <= end_time

#print(int(time.time()*1000))

def get_stock_info(market_code=market, stock_code=stock):
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en,zh-CN;q=0.9,zh;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Referer": "https://so.eastmoney.com/web/s?keyword={}".format(stock_code),
        "Sec-Fetch-Dest": "script",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "sec-ch-ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Google Chrome\";v=\"122\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\""
    }

    cookies = {
        "qgqp_b_id": "c9e1f0de0c01db9abc2465f80d3794b2",
        "websitepoptg_api_time": str(int(datetime.datetime.now().timestamp()*1000)),
        "st_si": "24299230542431",
        "st_asi": "delete",
        "st_pvi": "56325823352478",
        "st_sp": "2023-03-16%2014%3A39%3A48",
        "st_inirUrl": "https%3A%2F%2Fwww.baidu.com%2Flink",
        "st_sn": "5",
        "st_psi": "20240313103915664-118000300904-5261866992"
    }
    url = "https://push2.eastmoney.com/api/qt/stock/trends2/get"
    params = {
        "secid": "{}.{}".format(market_code, stock_code),
        "fields1": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58",
        "ut": "fa5fd1943c7b386f172d6893dbfba10b",
        "iscr": "0",
        "cb": "cb_1710297555909_59224578",
        "isqhquote": "",
        "cb_1710297555909_59224578": "cb_1710297555909_59224578"
    }
    response = requests.get(url, headers=headers, cookies=cookies, params=params)
    response_text = response.text
    response_text = response_text.replace("{}(".format(params.get("cb")), "").replace(");", "")
    #print(response_text)
    response_json = json.loads(response_text)
    data = response_json["data"]
    if data is None:
        print("")
        return
    name = response_json["data"]["name"]
    pre_price = float(response_json["data"]["prePrice"])
    trends = response_json["data"]["trends"]
    details = trends[len(trends) - 1].split(",") if len(trends) > 0 else ""
    price_text = ""
    move = ""
    color = 'white'
    if len(details) > 0:
        time_str = details[0].split(" ")[1]
        price = details[3]
        if float(price) < pre_price:
            color = 'green'
            move = '▼'
        elif float(price) > pre_price:
            color = 'red'
            move = '▲'

        price_text = "{}@{}".format(price, time_str)

    print("{}:{} {}| color={}".format(name, price_text, move, color))


current_time = datetime.datetime.now().time()

if is_time_between(datetime.time(9, 0), datetime.time(15, 0), current_time):
    get_stock_info()
elif is_time_between(datetime.time(15, 0), datetime.time(15, 30), current_time):
    #get_stock_info()
    print("购买国债逆回购!!!!|color=red")
elif is_time_between(datetime.time(15, 30), datetime.time(15, 40), current_time):
    get_stock_info()
else:
    #get_stock_info()
    print("")
