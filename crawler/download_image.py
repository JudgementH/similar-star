#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/11/10 22:07

'从数据库下载图片'

__author__ = 'Judgement'

import os
import traceback
from multiprocessing import Pool

import pymongo
import requests

client = pymongo.MongoClient()
db = client.similar_star_db
collection = db.star


def download(item, count):
    name = item['name']
    src = item['src']
    filename = name + '.' + src.split('.')[-1]
    path = os.path.join('../images', filename)
    if os.path.exists(path):
        print(name, src, 'Already Exist!!')
        collection.update({"_id": item['_id']}, {"$set": {"download": True}})
        return
    try:
        req = requests.get(src, timeout=60)
        req.raise_for_status()
        with open(path, 'wb') as f:
            f.write(req.content)
            print(count, name, src, 'Finished!!')
        req.close()
        collection.update({"_id": item['_id']}, {"$set": {"download": True}})
    except Exception:
        traceback.print_exc()
        print(name, src, 'Exception!!')
        if os.path.exists(path):
            os.remove(path)


if __name__ == '__main__':
    count = 0
    pool = Pool(5)
    for item in collection.find({}):
        if "download" not in item:
            pool.apply_async(download, args=(item, count))
            count = count + 1
    pool.close()
    pool.join()
