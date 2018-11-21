# #!/usr/bin/env python
# # !-*- coding:utf-8 -*-
# import smtplib
# from email.mime.text import MIMEText
# from email.header import Header
# !/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from util import PrintLog

LogObj = PrintLog.getInstance()

class Mail:
    def __init__(self):
        pass

    def mail(self, msg_content, receivers=[], receivers_EMail=[], subject=None):
        sender = 'OAMP_Anget'
        seder_EMail = 'yuantc@longrise.com.cn'
        seder_passwd = ''  # 发件人邮箱账号，正式环境时配置

        if not receivers:
            receivers = ['运维部人员']
        if not receivers_EMail:
            receivers_EMail = ['yuantc@longrise.com.cn']

        if subject is None:
            subject = "运维平台消息"

        ret = True
        try:
            msg = MIMEText(msg_content, 'plain', 'utf-8')
            msg['From'] = formataddr([sender, seder_EMail])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To'] = formataddr(["".join(receivers), "".join(receivers_EMail)])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject'] = subject  # 邮件的主题，也可以说是标题

            server = smtplib.SMTP("smtp.longrise.com.cn", 25)  # 发件人邮箱中的SMTP服务器，端口是25
            server.login(seder_EMail, seder_passwd)  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(seder_EMail, receivers_EMail, msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接
        except smtplib.SMTPException as e:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            print(e)
            ret = False
        return ret

    def sendMail(self, msg_content, receivers=[], receivers_EMail=[], subject=None):
        ret = self.mail(msg_content=msg_content, receivers=receivers, receivers_EMail=receivers_EMail, subject=subject)
        if ret:
            LogObj.info("邮件发送成功")
        else:
            LogObj.error("邮件发送失败")


def getInstance():
    return Mail()
