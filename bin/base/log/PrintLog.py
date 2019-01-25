#!/usr/bin/env python
# !-*- coding:utf-8 -*-
from bin.base.tool import Path
import logging
import logging.handlers
import os

logDirPath = Path.getInstance().logsDirPath

class PrintLog(logging.Logger):
    def __init__(self, filename=None):
        super(PrintLog, self).__init__(self)
        log_path = logDirPath + os.sep + "log.log"
        # formatter = logging.Formatter('[%(asctime)s] - %(filename)s [Line:%(lineno)d] - [%(levelname)s]-[thread:%(thread)s]-[process:%(process)s] - %(message)s')
        formatter = logging.Formatter('[%(levelname)8s]-[%(asctime)s]-%(filename)s :Line:%(lineno)d : %(message)s')
        # 日志文件名
        if filename is not None:
            log_path = logDirPath + os.sep + filename
            # 创建一个handler，用于写入日志文件 (每天生成1个，保留30天的日志)
            # fh = logging.handlers.TimedRotatingFileHandler(self.filename, 'D', 1, 30)
            # fh.suffix = "%Y%m%d-%H%M.log"
            # # fh = logging.handlers.RotatingFileHandler(self.log_all, mode='a', maxBytes=20 * 1024, backupCount=100, encoding=None, delay=0)
            # fh.setLevel(logging.DEBUG)
            # fh.setFormatter(formatter)  # 定义handler的输出格式
            # self.addHandler(fh)  # 给logger添加handler

            # # 创建一个handler，用于写入日志文件 (每天生成1个，保留30天的日志)
            # fh_all = logging.handlers.TimedRotatingFileHandler(self.log_all, 'D', 1, 30,encoding='utf-8')
            # fh_all.suffix = "%Y%m%d-%H%M.log"
        fh = logging.handlers.RotatingFileHandler(log_path, mode='a', maxBytes=1024 * 1024, backupCount=100, encoding='utf-8', delay=0)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)  # 定义handler的输出格式
        self.addHandler(fh)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)  # 定义handler的输出格式
        self.addHandler(ch)  # 给logger添加handler

        self.logging = logging
        # self.logging.Formatter = formatter
        # self.logging.handlers.RotatingFileHandler = fh
        # self.logging.handlers.StreamHandler = ch


def getInstance(filename=None):
    return PrintLog(filename)








