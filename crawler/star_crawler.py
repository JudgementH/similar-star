#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/11/10 16:49

'通过www.mingxing.com爬取明星图片放入数据库mongo'

__author__ = 'Judgement'

import os
import traceback

import requests
from bs4 import BeautifulSoup
import pymongo

client = pymongo.MongoClient()
db = client.similar_star_db
coll = db.star

if os.path.exists('../images') is False:
    os.makedirs('../images')

url = r'http://www.mingxing.com/ziliao'
for i in range(1, 276):
    try:
        url_ = r'http://www.mingxing.com/ziliao/index?&p={p}'.format(p=i)
        html = requests.get(url_, timeout=60).text
        soup = BeautifulSoup(html, 'html.parser')
        lis = soup.select(".page_starlist li")

        for li in lis:
            img = li.find('img')
            name = img['alt']
            src = img['src']
            try:
                if coll.find({"src": src}).count() == 0:
                    if coll.insert_one({"name": name, "src": src}):
                        print(name, src, 'Finished!!')
                else:
                    print(name, src, 'Exist!!')
            except Exception:
                traceback.print_exc()
    except Exception:
        print('connect error!!')
        continue
