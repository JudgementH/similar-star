#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/11/11 19:32

'创建索引'

__author__ = 'Judgement'

import pymongo
from elasticsearch import Elasticsearch

client = pymongo.MongoClient()
db = client.similar_star_db
collection = db.image

if __name__ == '__main__':
    es = Elasticsearch()
    index_mappings = {
        "mappings": {
            "properties": {
                "feature": {
                    "type": "dense_vector",
                    "dims": 2622,
                },
            }
        }
    }

    if es.indices.exists(index='star_index') is True:
        es.indices.delete(index="star_index")
    print("create star_index")
    es.indices.create(index='star_index', body=index_mappings)

    count = 0

    for image in collection.find():
        data = {
            "id": image["filename"],
            "feature": image["feature"],
        }
        res = es.index(index="star_index", id=image["filename"], body=data)
        print(count, res)

        count += 1
