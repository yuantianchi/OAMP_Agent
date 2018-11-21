#!/usr/bin/env python
# !-*- coding:utf-8 -*-
import logging
from util import Path

class PrintLog(logging.Logger):
    def __init__(self, filename=None):
        super(PrintLog, self).__init__(self)
        self.logPath = Path.getInstance().logsDirPath
        self.filename = filename
        log_all = self.logPath + "log.log"

        if self.filename is not None:
            log_all = self.logPath + filename

        # self.logger = logging.getLogger(log_all)  ##设置日志输出文件
        # self.logger.setLevel(logging.DEBUG)  ##设置日志输出等级，即只有日志级别大于等于该级别的日志才会输出

        # 建立一个filehandler来把日志记录在文件里，级别为DEBUG以上
        fh = logging.FileHandler(log_all)
        fh.setLevel(logging.DEBUG)

        # 建立一个streamhandler来把日志打在CMD窗口上，级别为info以上
        ch =logging.StreamHandler()
        ch.setLevel(logging.INFO)

        #设置日志格式
        logFormat="[%(levelname)8s] - [%(asctime)s] - %(filename)s[line:%(lineno)d] - %(message)s"
        consoleFormat="[%(levelname)8s] - %(message)s"

        logformatter = logging.Formatter(logFormat)
        consoleformatter= logging.Formatter(consoleFormat)

        fh.setFormatter(logformatter)
        ch.setFormatter(consoleformatter)
        self.addHandler(ch)
        self.addHandler(fh)

def getInstance(filename=None):
    return PrintLog(filename)

if __name__ == '__main__':
    getInstance().info("xxx")
