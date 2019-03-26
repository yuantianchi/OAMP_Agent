#!/usr/bin/env python
# !-*- coding:utf-8 -*-
import bin
from bin.base.sys import PR
from bin.init import Init
from bin.logic.func import Nginxfunc, TomcatFun
from bin.base.tool import Mail
from bin.base.log import PrintLog

T = TomcatFun.getInstance()
M = Mail.getInstance()
from bin.base.tool import FuncRedisModifier


LogObj = PrintLog.getInstance()

class AgentTomcatFunc(object):
    def __init__(self):
        pass
        # 重启项目对应的所有tomcat

    def restartOneTomcat(self, info):
        opt_id = info.get("opt_id", '1')
        # 1、调用参数和方法写入redis
        # 2、等待redis执行
        _PR = PR.getInstance()
        tomcatInfo = info.get("tomcatInfo")
        if len(tomcatInfo) < 1:
            return _PR.setCode(PR.Code_ERROR).setMsg('重启失败，tomcatInfo信息为空')
        tomcatName = tomcatInfo['name']
        opt_id = info.get("opt_id", '1')
        # 1、调用参数和方法写入redis
        # 2、等待redis执行
        redis_conf_info = bin.CONF_INFO.get('redis')
        redis_key = 'restartOneTomcat_' + tomcatName
        fun_redis_ins = FuncRedisModifier.getInstance(redis_conf_info, redis_key)

        if not fun_redis_ins.init_redis() is None:
            return _PR.setCode(PR.Code_ERROR).setMsg('容器%s 还在重启中，请稍后' % tomcatName)

        fun_redis_ins.set_func_method('restart_one_tomcat', info)
        fun_redis_ins.set_func_opt_id(opt_id)
        fun_redis_ins.set_func_state_start()
        _result = fun_redis_ins.set_func_summary('重启容器%s，开始执行' % tomcatName).set_redis()
        if _result:
            return _PR.setCode(PR.Code_OK).setMsg('重启容器%s 命令启动成功' % tomcatName)
        else:
            return _PR.setCode(PR.Code_ERROR).setMsg('重启容器%s 操作执行错误:redis 存储方法体失败' % tomcatName)

    # 后台调用--重启项目的某个容器
    def _restart_one_tomcat(self, redis_info, redis_k):
        try:
            run_redis_info = FuncRedisModifier.getInstance(redis_k=redis_k, redis_info=redis_info).init_redis()
            func_data = run_redis_info.get_func_method_par()
            tomcatInfo = func_data.get("tomcatInfo")
            tomcatName = tomcatInfo['name']
            run_redis_info.set_func_summary('正在执行重启容器%s' % tomcatName).set_redis()
            restart_result = TomcatFun.getInstance().restartOneTomcat(tomcatName)
        except Exception as e:
            LogObj.error('重启容器%s失败，等待重试' % (tomcatName))
            run_redis_info.set_func_state_start()
            run_redis_info.set_func_summary('重启容器%s失败，等待重试' % tomcatName).set_redis()

        if restart_result:
            run_redis_info.set_func_state_end()
            run_redis_info.set_func_summary('重启容器%s成功，执行成功' % tomcatName).set_redis()
        else:
            run_redis_info.set_func_state_start()
            run_redis_info.set_func_summary('重启容器%s失败，等待重试' % tomcatName).set_redis()



    # 单独停止某个tomcat
    def stopOneTomcat(self, tomcatInfo):
        _PR = PR.getInstance()
        tomcatName = tomcatInfo["name"]
        nginxPort = tomcatInfo["port"]

        if not T.stopTomcat(tomcatName, self.maxRestartCount):
            return _PR.setCode(PR.Code_OK).setMsg('stop %s failed' % (tomcatName))
        else:
            N.closeNginxUpstream(nginxPort)
            return _PR.setCode(PR.Code_OK).setMsg('stop %s success' % (tomcatName))

    # 单独启动某个tomcat
    def startOneTomcat(self, tomcatInfo):
        _PR = PR.getInstance()
        tomcatName = tomcatInfo["name"]
        nginxPort = tomcatInfo["port"]
        if not T.startTomcat(tomcatName, self.maxRestartCount):
            return _PR.setMsg("start %s failed" % (tomcatName)).setCode(PR.Code_ERROR)
        else:
            N.openNginxUpstream(nginxPort)
            return _PR.setMsg("start %s success" % (tomcatName)).setCode(PR.Code_OK)


def getInstance():
    return AgentTomcatFunc()
