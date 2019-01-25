#!/usr/bin/env python
# !-*- coding:utf-8 -*-
import json
import redis


class Redis(object):
    def __init__(self, host, port, db, password):
        pool = redis.ConnectionPool(max_connections=100, host=host, port=port, db=db, password=password)
        self.redis = redis.StrictRedis(connection_pool=pool)

    def setJson(self, key, value, ex):
        data = {}
        if value is None:
            return None
        for k in value.keys():
            val = value.get(k)
            if val is None:
                continue
            if val is True:
                val = 1
            data[k] = val
        return self.redis.set(name=key, value=json.dumps(data, ensure_ascii=False), ex=ex)

    def delJson(self, key):
        return self.redis.delete(key)

    def getJson(self, key):
        redis_data = self.redis.get(key)
        if redis_data is None:
            return None
        return json.loads(str(redis_data, encoding="utf-8"))


def getInstance(host='127.0.0.1', port=6379, db=0, password=None):
    return Redis(host=host, port=port, db=db, password=password)
