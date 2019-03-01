#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin.base.log import PrintLog
import bin
from bin.base.tool import File, JsonFileFunc, Path
import threading
from bin.logic import Inner_logic
import time
from bin.base.tool import FuncRedisModifier
import os
from bin.base.tool import Mail
from bin.base.tool import FuncRecordModifier

LogObj = PrintLog.getInstance()
jff = JsonFileFunc.getInstance()
p = Path.getInstance()
F = File.getInstance()


# 初始化配置文件到缓存中，创建项目更新文件存放目录
class Init(object):
    def __init__(self):
        self.confPath = p.confDirPath + os.sep + "conf.json"
        self.ProjectConfigPath = p.confDirPath + os.sep + "projectInfo.json"
        # self.runTimePath = p.projectDirPath + os.sep + "runtime" + os.sep + "runtime.json"

    def rebuild_memory_val(self):
        bin.CONF_INFO = jff.readFile(self.confPath)
        bin.PROJECT_INFO = jff.readFile(self.ProjectConfigPath)

    def __reset_exec_func_state(self):
        if bin.CONF_INFO is not None and bin.CONF_INFO.get('redis') is not None and bin.PROJECT_INFO is not None:
            redis_info = bin.CONF_INFO.get('redis')
            for k in bin.PROJECT_INFO.keys():
                func_redis_ins = FuncRedisModifier.getInstance(redis_k=k, redis_info=redis_info).init_redis()
                if func_redis_ins is None:
                    continue
                func_redis_ins.set_func_state_start().set_redis()
        else:
            LogObj.warn('projectInfo 文件不存在')
            # 发邮件的！！！！ fixed 2019年1月22日14:55:04
            # Mail.getInstance().sendMail("OAMP_agent启动项目功能执行，projectInfo 文件不存在！")
        return True

    def exec(self):
        LogObj.info('%s 开始运行' % threading.current_thread().name)
        try:
            inner_logic_ins = Inner_logic.getInstance()
            if not self.__reset_exec_func_state():
                return 0
            while True:
                if bin.CONF_INFO is not None and bin.CONF_INFO.get('redis') is not None and bin.PROJECT_INFO is not None:
                    redis_info = bin.CONF_INFO.get('redis')
                    for k in bin.PROJECT_INFO.keys():
                        func_redis_ins = FuncRedisModifier.getInstance(redis_k=k, redis_info=redis_info).init_redis()
                        if func_redis_ins is None:
                            # LogObj.debug('%s项目暂无待执行的方法'% str(k))
                            continue

                        method = func_redis_ins.get_func_method()
                        func_state = func_redis_ins.get_func_state()
                        fun_summary = func_redis_ins.get_func_summary()
                        exec_count = func_redis_ins.get_func_exec_count()
                        opt_id = func_redis_ins.get_func_opt_id()
                        LogObj.debug('opt_is is %s' % opt_id)
                        LogObj.debug('exec_count is %d' % exec_count)

                        func_record_ins = FuncRecordModifier.getInstance(projectName=k)
                        record_is_normal = FuncRecordModifier.normal
                        record_is_finish = FuncRecordModifier.not_finished

                        func_record_ins.setOperateId(opt_id)

                        if exec_count > 3:
                            func_state = FuncRedisModifier.REDIS_FUNC_STATE_FAILED
                            summary = '%s项目，执行%s方法未成功超过3次,将结束执行' % (str(k), str(method))
                            LogObj.error(summary)

                        if FuncRedisModifier.REDIS_FUNC_STATE_NONE == func_state:
                            func_redis_ins.add_exec_count().set_redis()
                            summary = '未正常实例化功能redis对象'
                            LogObj.error(summary)

                        elif FuncRedisModifier.REDIS_FUNC_STATE_RUN == func_state:
                            summary = '%s项目,执行%s方法,项目状态为执行中，操作相关描述为:%s' % (str(k), method, str(fun_summary))
                            LogObj.debug(summary)

                        elif FuncRedisModifier.REDIS_FUNC_STATE_END == func_state:
                            record_is_finish = FuncRecordModifier.finished
                            func_redis_ins.del_redis()
                            summary = '%s项目,执行%s方法,项目状态为方法执行完成,操作相关描述为:执行成功' % (str(k), method)
                            LogObj.info(summary)

                        elif FuncRedisModifier.REDIS_FUNC_STATE_FAILED == func_state:
                            record_is_finish = FuncRecordModifier.finished
                            record_is_normal = FuncRecordModifier.not_Normal
                            func_redis_ins.del_redis()
                            summary = '%s项目,执行%s方法,项目状态为方法执行失败,操作相关描述为:执行失败' % (str(k), method)
                            LogObj.error(summary)

                        elif FuncRedisModifier.REDIS_FUNC_STATE_START == func_state:
                            t = threading.Thread(target=getattr(inner_logic_ins, method), args=(redis_info, k,))
                            t.start()
                            func_redis_ins.set_func_state_run().set_redis()
                            summary = '%s项目,执行%s方法,项目状态为方法执行开始,操作相关描述为:执行开始' % (str(k), method)
                            LogObj.info(summary)

                        else:
                            func_redis_ins.add_exec_count().set_redis()
                            record_is_normal = FuncRecordModifier.not_Normal
                            summary = '%s项目,执行%s方法,项目状态未知,操作相关描述为:功能redis对象非正常状态' % (str(k), method)
                            LogObj.error(summary)

                        func_record_ins.setIs_finished(record_is_finish)
                        func_record_ins.setIs_normal(record_is_normal)
                        func_record_ins.setSummary(summary)
                        func_record_ins.set_FuncRecord()
                        # fixed 等待后续操作内容处理
                        # 修改执行结果内容
                time.sleep(3)
        except Exception as e:
            LogObj.critical("redis 连接异常失败，请检查配置信息，和网络情况")
            bin.REDIS_FUNC_RECEIVER_STATUS=0
            # Mail.getInstance().sendMail("服务器%s agent运行时redis 连接异常失败，请检查配置信息，和网络情况"%(local_ip))



    # 初始化redis 方法接收者
    def init_redis_func_receiver(self):
        if bin.REDIS_FUNC_RECEIVER_STATUS != 1:
            bin.REDIS_FUNC_RECEIVER_STATUS=1
        t = threading.Thread(target=self.exec, name='threadFuncReceiverTask', daemon=True)
        t.start()


def getInstance():
    return Init()
