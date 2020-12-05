#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/11/11 21:24

' 余弦相似度的es应用参考文章'
'https://www.elastic.co/cn/blog/text-similarity-search-with-vectors-in-elasticsearch'
'https://www.elastic.co/guide/en/elasticsearch/reference/7.3/query-dsl-script-score-query.html#vector-functions'

__author__ = 'Judgement'

from elasticsearch import Elasticsearch


def feature_query(feature: list, size=10) -> list:
    script_query = {
        "script_score": {
            "query": {"match_all": {}},
            "script": {
                "source": "cosineSimilarity(params.query_vector, doc['feature'])",
                "params": {"query_vector": feature}
            }
        }
    }
    es = Elasticsearch()
    searched = es.search(index="star_index", body={
        "size": size,
        "query": script_query
    })

    results = []
    for hit in searched["hits"]["hits"]:
        star = {'name': hit['_id'].split(".")[0], 'score': hit["_score"]}
        results.append(star)
    return results
