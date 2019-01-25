#!/usr/bin/env python
# !-*- coding:utf-8 -*-
import bin
from bin.base.tool import Time
from bin.base.tool import Path
from bin.base.tool import Redis
from bin.base.tool import JsonFileFunc
from bin.base.tool import FuncRedisModifier

not_Normal = 0
normal = 1
not_finished = 0
finished = 1

P = Path.getInstance()
JF = JsonFileFunc.getInstance()


class FuncRecordFileModifier:

    def __init__(self, projectName):
        self.operateId = ''
        self.projectName = projectName
        self.summary = ''
        self.is_finished = not_finished
        self.last_modify_time = ''
        self.is_normal = normal

        local_ip = bin.CONF_INFO.get('localIp')
        redis_info = bin.CONF_INFO.get('redis')
        host = redis_info.get('host', '127.0.0.1')
        password = redis_info.get('password')
        port = redis_info.get('port', 6379)

        self.redis_ins = Redis.getInstance(db=FuncRedisModifier.REDIS_FUNC_DB, host=host, port=port, password=password)
        self.redis_store_key = str(local_ip) + '_func_record_' + str(self.projectName)

    def getFuncRecord(self):
        FuncRecord = self.redis_ins.getJson(key=self.redis_store_key)
        if FuncRecord is None:
            return None
        self.operateId = FuncRecord.get('operateId')
        self.summary = FuncRecord.get('summary')
        self.is_finished = FuncRecord.get('is_finished')
        self.last_modify_time = FuncRecord.get('last_modify_time')
        self.is_normal = FuncRecord.get('is_normal')
        return self.json()

    def set_FuncRecord(self):
        self.last_modify_time = Time.getIntance().getCurrentTime()
        return self.redis_ins.setJson(key=self.redis_store_key, value=self.json(), ex=2592000)

    def json(self):
        item = {
            'operateId': self.operateId,
            'summary': self.summary,
            'is_finished': self.is_finished,
            'last_modify_time': self.last_modify_time,
            'is_normal': self.is_normal,
        }
        return item

    def setOperateId(self, operateId):
        self.operateId = operateId

    def setSummary(self, summary):
        self.summary = summary
        return self

    def setIs_finished(self, is_finished):
        self.is_finished = is_finished
        return self

    def setIs_normal(self, is_normal):
        self.is_normal = is_normal
        return self

    def getOperateId(self):
        return self.operateId

    def getSummary(self):
        return self.summary

    def getIs_finished(self):
        return self.is_finished

    def getIs_normal(self, is_normal):
        return self.is_normal


def getInstance(projectName):
    return FuncRecordFileModifier(projectName)
