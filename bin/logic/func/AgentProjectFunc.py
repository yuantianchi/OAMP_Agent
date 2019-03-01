#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import bin
from bin.base.sys import PR
from bin.init import Init
from bin.logic.func import ProjectFunc
from bin.logic.func import TomcatFun
from bin.base.log import PrintLog
from bin.base.tool import FuncRedisModifier
from bin.base.tool import File
from bin.base.tool import JsonFileFunc
from bin.base.tool import Path
from bin.base.tool import FuncRecordModifier
import os
import sys

LogObj = PrintLog.getInstance()
jff = JsonFileFunc.getInstance()
p = Path.getInstance()
F = File.getInstance()


class AgentProjectFunc(object):
    def __init__(self):
        pass

    # 查询项目相关操作的状态
    def getProjectStatus(self, info):
        _PR = PR.getInstance()
        projectName = info.get("projectName", None)
        if not projectName:
            return _PR.setCode(PR.Code_ERROR).setMsg('请求参数错误，参数projectName不能为空')
        if projectName not in bin.PROJECT_INFO:
            return _PR.setCode(PR.Code_ERROR).setMsg('更新项目失败，angent中还未配置%s项目信息' % projectName).setData(projectName)
        record = FuncRecordModifier.getInstance(projectName).getFuncRecord()
        if record is None:
            return _PR.setCode(PR.Code_ERROR).setMsg('未能找到%s项目运行状态记录' % str(projectName))
        return _PR.setCode(PR.Code_OK).setData(record).setMsg('查询项目运行状态操作成功')

    # 以增量形式初始化项目配置和conf.json信息
    def modifyConfInfo(self, info):
        ProjectConfigPath = p.confDirPath + os.sep + "projectInfo.json"
        confJsonPath = p.confDirPath + os.sep + "conf.json"
        if bin.PROJECT_INFO is None:
            bin.PROJECT_INFO = {}
        projectName = list(info)[0]
        projectDataInfo = info.get(projectName, None)
        if projectDataInfo is None:
            return False
        confJsonInfo = {
            'nginxUpstreamPath': projectDataInfo.get('upstream_conf_file', '/usr/local/nginx/conf/nginx.conf'),
            'redis': {
                'host': projectDataInfo.get('redis_ip', '127.0.0.1'),
                'password': projectDataInfo.get('redis_password', 'longrise'),
                'port': projectDataInfo.get('redis_port', 6379)
            },
            'localIp': projectDataInfo.get('local_ip', '127.0.0.1')
        }
        noNeedKey = ['upstream_conf_file', 'redis_ip', 'redis_password', 'redis_port', 'local_ip']
        for i in noNeedKey:
            if i in projectDataInfo.keys():
                projectDataInfo.pop(i)
        projectInfo = {projectName: projectDataInfo}
        bin.PROJECT_INFO.update(projectInfo)
        bin.CONF_INFO.update(confJsonInfo)
        if not jff.writeFile(confJsonPath, bin.CONF_INFO):
            return False
        return jff.writeFile(ProjectConfigPath, bin.PROJECT_INFO)

    # 初始化项目配置
    def initProjectConf(self, info):
        _PR = PR.getInstance()
        confData = info.get('confData')
        if not self.modifyConfInfo(confData):
            return _PR.setCode(PR.Code_ERROR).setMsg('initialize project configuration information Failed')
        Init.getInstance().rebuild_memory_val()
        if bin.REDIS_FUNC_RECEIVER_STATUS != 1:
            Init.getInstance().init_redis_func_receiver()
        # 创建目录
        for k in confData.keys():
            backupFilePath = confData.get(k).get('backupFilePath')
            File.getInstance().makedir(backupFilePath)
        result = {'ProjectInfo': bin.PROJECT_INFO}
        return _PR.setData(result).setCode(PR.Code_OK).setMsg('initialize project configuration information is complete')

    # 更新LEAP项目资源
    def replaceResource(self, info):
        _PR = PR.getInstance()
        projectName = info.get("projectName")
        projectVersion = info.get("projectVersion")
        backupFilePath = bin.PROJECT_INFO.get(projectName)["backupFilePath"]
        updateFilePath = backupFilePath + os.sep + str(projectVersion) + ".tar.gz"

        if not projectName or not projectVersion:
            return _PR.setCode(PR.Code_ERROR).setMsg('更新项目失败，项目名或项目版本为空')
        if projectName not in bin.PROJECT_INFO:
            return _PR.setCode(PR.Code_ERROR).setMsg('更新项目失败，agent中还未配置%s项目信息' % projectName)
        if not F.isExitsFile(updateFilePath):
            LogObj.info("%s项目的%s版本的更新资源不存在" % (projectName, projectVersion))
            return _PR.setCode(PR.Code_ERROR).setMsg("%s项目的%s版本的更新资源不存在" % (projectName, str(projectVersion)))

        opt_id = info.get("opt_id", '1')
        # 1、调用参数和方法写入redis
        # 2、等待redis执行
        redis_conf_info = bin.CONF_INFO.get('redis')
        fun_redis_ins = FuncRedisModifier.getInstance(redis_conf_info, projectName)
        if not fun_redis_ins.init_redis() is None:
            return _PR.setCode(PR.Code_ERROR).setMsg('当前项目有操作未完成，请稍后')
        fun_redis_ins.set_func_method('project_replace_resource', info)
        fun_redis_ins.set_func_opt_id(opt_id)
        fun_redis_ins.set_func_state_start()
        _result = fun_redis_ins.set_func_summary('LEAP资源开始更新').set_redis()

        if _result:
            result = {"projectName": projectName, "projectVersion": projectVersion}
            return _PR.setCode(PR.Code_OK).setData(result).setMsg('启动项目资源替换命令成功')
        else:
            return _PR.setCode(PR.Code_ERROR).setMsg('替换资源操作执行错误:redis 存储方法体失败')

    # 后台进程调用--更新资源
    def _project_replace_resource(self, redis_info, redis_k):
        run_redis_info = FuncRedisModifier.getInstance(redis_k=redis_k, redis_info=redis_info).init_redis()
        func_data = run_redis_info.get_func_method_par()
        run_redis_info.set_func_summary('正在执行%s项目资源替换' % str(redis_k)).set_redis()

        projectName = func_data.get("projectName")
        projectVersion = func_data.get("projectVersion")

        pF = ProjectFunc.getInstance(projectName)
        pF.handleResource(projectVersion)
        result = pF.replaceLEAPResource(projectVersion)

        if result:
            run_redis_info.set_func_state_end()
            run_redis_info.set_func_summary('执行%s项目资源替换，执行成功' % str(redis_k)).set_redis()
        else:
            run_redis_info.set_func_state_start()
            run_redis_info.set_func_summary('执行%s项目资源替换，执行失败，等待重试' % str(redis_k)).set_redis()

    # 重启项目对应的所有tomcat
    def restartProject(self, info):
        _PR = PR.getInstance()
        projectName = info.get("projectName")

        if not projectName:
            return _PR.setCode(PR.Code_ERROR).setMsg('重启项目失败，项目名为空').setData(projectName)
        if projectName not in bin.PROJECT_INFO:
            return _PR.setCode(PR.Code_ERROR).setMsg('重启项目失败，angent中还未配置%s项目信息' % projectName).setData(projectName)

        opt_id = info.get("opt_id", '1')
        # 1、调用参数和方法写入redis
        # 2、等待redis执行
        redis_conf_info = bin.CONF_INFO.get('redis')
        fun_redis_ins = FuncRedisModifier.getInstance(redis_conf_info, projectName)
        if not fun_redis_ins.init_redis() is None:
            return _PR.setCode(PR.Code_ERROR).setMsg('当前项目有操作未完成，请稍后')
        fun_redis_ins.set_func_method('project_restart', info)
        fun_redis_ins.set_func_opt_id(opt_id)
        fun_redis_ins.set_func_state_start()
        _result = fun_redis_ins.set_func_summary('%s项目重启，开始执行' % projectName).set_redis()
        if _result:
            result = {"projectName": projectName}
            return _PR.setCode(PR.Code_OK).setData(result).setMsg('项目重启命令启动成功')
        else:
            return _PR.setCode(PR.Code_ERROR).setMsg('项目重启操作执行错误:redis 存储方法体失败')

    # 后台进程调用--重启项目
    def _project_restart(self, redis_info, redis_k):
        run_redis_info = FuncRedisModifier.getInstance(redis_k=redis_k, redis_info=redis_info).init_redis()
        func_data = run_redis_info.get_func_method_par()
        run_redis_info.set_func_summary('正在执行%s项目重启' % str(redis_k)).set_redis()

        projectName = func_data.get("projectName")
        restart_pr = TomcatFun.getInstance().restartProjectTom(projectName)

        if restart_pr.getCode() == PR.Code_OK:
            run_redis_info.set_func_state_end()
            run_redis_info.set_func_summary('%s项目项目重启，执行成功' % str(redis_k)).set_redis()
        else:
            run_redis_info.set_func_state_start()
            run_redis_info.set_func_summary('%s项目项目重启，执行失败，等待重试' % str(redis_k)).set_redis()

    # 更新项目
    def updateProject(self, info):
        _PR = PR.getInstance()
        projectName = info.get("projectName", None)
        projectVersion = info.get("projectVersion", None)
        backupFilePath = bin.PROJECT_INFO.get(projectName)["backupFilePath"]
        updateFilePath = backupFilePath + os.sep + str(projectVersion) + ".tar.gz"
        opt_id = info.get("opt_id", '1')
        # 1、调用参数和方法写入redis
        # 2、等待redis执行
        projectVersion = info.get("projectVersion", None)
        result = {"projectName": projectName, "projectVersion": projectVersion}

        if not projectName or not projectVersion:
            return _PR.setCode(PR.Code_ERROR).setMsg('更新项目失败，项目名或项目版本为空').setData(projectName)
        if projectName not in bin.PROJECT_INFO:
            return _PR.setCode(PR.Code_ERROR).setMsg('更新项目失败，agent中还未配置%s项目信息' % projectName).setData(projectName)
        if not F.isExitsFile(updateFilePath):
            return _PR.setCode(PR.Code_ERROR).setMsg("%s项目的%s版本的更新资源不存在" % (projectName, str(projectVersion)))
        redis_conf_info = bin.CONF_INFO.get('redis')
        fun_redis_ins = FuncRedisModifier.getInstance(redis_conf_info, projectName)
        if not fun_redis_ins.init_redis() is None:
            return _PR.setCode(PR.Code_ERROR).setMsg('当前项目有操作未完成，请稍后')
        fun_redis_ins.set_func_method('project_update', info)
        fun_redis_ins.set_func_opt_id(opt_id)
        fun_redis_ins.set_func_state_start()
        _result = fun_redis_ins.set_func_summary('%s项目更新开始执行' % projectName).set_redis()
        if _result:
            result = {"projectName": projectName}
            return _PR.setCode(PR.Code_OK).setData(result).setMsg('项目更新命令启动成功')
        else:
            return _PR.setCode(PR.Code_ERROR).setMsg('项目更新操作执行错误:redis 存储方法体失败')

    # 后台进程调用--项目更新
    def _project_update(self, redis_info, redis_k):
        run_redis_info = FuncRedisModifier.getInstance(redis_k=redis_k, redis_info=redis_info).init_redis()
        func_data = run_redis_info.get_func_method_par()
        run_redis_info.set_func_summary('正在执行%s项目更新' % str(redis_k)).set_redis()
        projectName = func_data.get("projectName")
        projectVersion = func_data.get("projectVersion", None)
        PF = ProjectFunc.getInstance(projectName)
        update_pr = PF.updateProject(projectVersion)

        if update_pr.getCode() == PR.Code_OK:
            run_redis_info.set_func_state_end()
            run_redis_info.set_func_summary('%s项目项目更新执行成功' % str(redis_k)).set_redis()
        else:
            run_redis_info.set_func_state_start()
            run_redis_info.set_func_summary('%s项目项目更新执行失败，等待重试' % str(redis_k)).set_redis()


def getInstance():
    return AgentProjectFunc()
