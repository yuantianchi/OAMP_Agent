#!/usr/bin/env python
# !-*- coding:utf-8 -*-
import bin
from bin.base.tool import Redis
from bin.base.tool import Mail
import sys

REDIS_FUNC_DB = 1
REDIS_FUNC_STATE_NONE = -2
REDIS_FUNC_STATE_START = -1
REDIS_FUNC_STATE_RUN = 0
REDIS_FUNC_STATE_END = 1
REDIS_FUNC_STATE_FAILED = 2


class FuncRedisModifier(object):
    def __init__(self, redis_info=None, redis_k=None):
        from bin.base.log import PrintLog
        L = PrintLog.getInstance()
        local_ip = bin.CONF_INFO.get('localIp')
        host = redis_info.get('host', '127.0.0.1')
        password = redis_info.get('password')
        port = redis_info.get('port', 6379)

        self.redis_ins = Redis.getInstance(db=REDIS_FUNC_DB, host=host, port=port, password=password)
        self.redis_k = redis_k
        self.fun_state = REDIS_FUNC_STATE_NONE
        self.fun_summary = ''
        self.exec_count = 0
        self.method = ''
        self.method_par = None
        self.opt_id = None
        self.default_prefix=str(local_ip) + '_'
        self.redis_store_key = self.default_prefix + str(self.redis_k)

    def json(self):
        item = {
            'method': self.method,
            'method_par': self.method_par,
            'exec_count': self.exec_count,
            'func_state': self.fun_state,
            'func_summary': self.fun_summary,
            'opt_id': self.opt_id
        }
        return item

    def set_func_method(self, method, method_par=None):
        if method_par is not None:
            self.method_par = method_par
        self.method = method
        return self

    def set_func_method_par(self, method_par):
        self.method_par = method_par
        return self

    def set_func_opt_id(self, opt_id):
        self.opt_id = opt_id
        return self

    def set_redis_k(self, k):
        self.redis_k = k
        return self

    def set_func_state(self, state):
        self.fun_state = state
        return self

    def set_func_state_start(self):
        self.fun_state = REDIS_FUNC_STATE_START
        return self

    def set_func_state_run(self):
        self.fun_state = REDIS_FUNC_STATE_RUN
        return self

    def set_func_state_end(self):
        self.fun_state = REDIS_FUNC_STATE_END
        return self

    def set_func_summary(self, summary):
        self.fun_summary = summary
        return self

    def set_func_exec_count(self, count):
        self.exec_count = count
        return self

    def add_exec_count(self):
        self.exec_count += 1
        return self

    def init_redis(self):
        redis_data = self.redis_ins.getJson(key=self.redis_store_key)
        if redis_data is None:
            return None
        self.fun_state = redis_data.get('func_state')
        self.fun_summary = redis_data.get('func_summary')
        self.exec_count = redis_data.get('exec_count')
        self.method = redis_data.get('method')
        self.method_par = redis_data.get('method_par')
        self.opt_id = redis_data.get('opt_id')
        return self

    def get_redis_keys(self):
        redis_key = self.redis_ins.fuzzy_getKeys(key=self.redis_store_key)
        redis_key=[str(i)[len(self.default_prefix):] for i in redis_key]
        return redis_key

    def set_redis(self):
        return self.redis_ins.setJson(key=self.redis_store_key, value=self.json(), ex=36000)

    def del_redis(self):
        return self.redis_ins.delJson(key=self.redis_store_key)

    def get_func_method(self):
        return self.method

    def get_func_method_par(self):
        return self.method_par

    def get_func_exec_count(self):
        return self.exec_count

    def get_func_summary(self):
        return self.fun_summary

    def get_func_state(self):
        return self.fun_state

    def get_func_opt_id(self):
        return self.opt_id


def getInstance(redis_info, redis_k):
    return FuncRedisModifier(redis_info=redis_info, redis_k=redis_k)
