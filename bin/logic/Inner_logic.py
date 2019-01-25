#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin.base.sys import PR
from bin.init import Init
from bin.logic.func import ProjectFunc, Nginxfunc, TomcatFun
from bin.base.tool import Mail
from bin.base.log import PrintLog

from bin.logic.func import AgentProjectFunc

T = TomcatFun.getInstance()
M = Mail.getInstance()

N = Nginxfunc.getInstance()
LogObj = PrintLog.getInstance()
_PR = PR.getInstance()


class Inner_logic():
    def __init__(self):
        pass

    def project_replace_resource(self,redis_info,k):
        return AgentProjectFunc.getInstance()._project_replace_resource(redis_info=redis_info,redis_k=k)

    def project_restart(self,redis_info,k):
        return AgentProjectFunc.getInstance()._project_restart(redis_info=redis_info,redis_k=k)

    def project_update(self, redis_info, k):
        return AgentProjectFunc.getInstance()._project_update(redis_info=redis_info,redis_k=k)

def getInstance():
    return Inner_logic()
